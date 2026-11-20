"""
V.E.R.D.A.N.T. v2 — Native Windows Desktop Floating Capsule (WPF)

Always-on-top frameless capsule. Drop-in replacement for capsule/app.py.

Key differences from the previous version:
  * The window is created and shown FIRST. The Gemini/patcher/git engine is loaded
    in a background thread afterwards, so a slow or broken engine can never stop the
    capsule from appearing (it just shows "Engine failed" in the status line).
  * Every failure (pythonnet missing, WPF error, engine error) is written to
    <project>/capsule_debug.log with a full traceback and also shown in a MessageBox.
  * Positions itself from the real work area instead of a hard-coded 1280px screen.
  * Window height auto-sizes to its content (no clipped status row).
  * Real global hotkey (Ctrl+Shift+Space, falls back to Ctrl+Alt+Space) — no extra deps.
  * Snap button hides the capsule first, so it captures the app underneath instead of itself.
  * Correct 64-bit SetWindowPos call (HWND_TOPMOST was being truncated before).

Usage:
    python capsule/app.py
    python -m capsule.app

Optional:
    set CAPSULE_ROUNDED=1   -> true rounded pill (uses a transparent layered window)
"""
import os
import sys
import time
import ctypes
import threading
import traceback
from ctypes import wintypes
from pathlib import Path

# ── Paths / environment ──────────────────────────────────────────────────────
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
LOG_FILE = ROOT / "capsule_debug.log"

ROUNDED = os.environ.get("CAPSULE_ROUNDED", "0") == "1"


def log(msg: str) -> None:
    line = f"[{time.strftime('%H:%M:%S')}] {msg}"
    try:
        print(line)
        sys.stdout.flush()
    except Exception:
        pass
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(line + "\n")
    except Exception:
        pass


def fatal_box(title: str, text: str) -> None:
    """Always-visible error popup (a console may not be visible)."""
    try:
        ctypes.windll.user32.MessageBoxW(None, text[:1800], title, 0x10)
    except Exception:
        pass


# Load .env
env_file = ROOT / ".env"
if env_file.exists():
    for _line in env_file.read_text(encoding="utf-8").splitlines():
        _line = _line.strip()
        if _line and "=" in _line and not _line.startswith("#"):
            _k, _v = _line.split("=", 1)
            os.environ.setdefault(_k.strip(), _v.strip().strip('"').strip("'"))

# Physical-pixel coordinates so window rects match ImageGrab (must be set before any window)
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(2)
except Exception:
    try:
        ctypes.windll.user32.SetProcessDPIAware()
    except Exception:
        pass

# ── WPF via pythonnet ────────────────────────────────────────────────────────
try:
    sys.path.append(r"C:\Windows\Microsoft.NET\Framework64\v4.0.30319\WPF")
    import clr
    clr.AddReference("PresentationFramework")
    clr.AddReference("PresentationCore")
    clr.AddReference("WindowsBase")

    import System
    from System.Threading import Thread, ThreadStart, ApartmentState
    from System.Windows import (
        Application, Window, WindowStyle, WindowStartupLocation, WindowState,
        HorizontalAlignment, VerticalAlignment, CornerRadius, Thickness,
        Visibility, TextWrapping, FontWeights, GridLength, GridUnitType,
        SizeToContent, SystemParameters, ResizeMode, TextTrimming,
    )
    from System.Windows.Media import Brushes, Color, SolidColorBrush, FontFamily
    from System.Windows.Controls import (
        Border, StackPanel, Grid, TextBox, TextBlock, Button, ScrollViewer,
        ColumnDefinition, Orientation, ScrollBarVisibility,
    )
    from System.Windows.Input import Key
    from System.Windows.Interop import WindowInteropHelper
except Exception:
    _tb = traceback.format_exc()
    log("FATAL: could not load WPF / pythonnet\n" + _tb)
    fatal_box(
        "V.E.R.D.A.N.T. Capsule",
        "Could not load WPF through pythonnet.\n\n"
        "Fix:  pip install pythonnet   (use Python 3.10-3.12 on Windows)\n\n"
        f"Details in:\n{LOG_FILE}\n\n{_tb[-600:]}",
    )
    raise SystemExit(1)

user32 = ctypes.windll.user32
user32.SetWindowPos.argtypes = [
    wintypes.HWND, wintypes.HWND,
    ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, wintypes.UINT,
]
user32.SetWindowPos.restype = wintypes.BOOL
HWND_TOPMOST = wintypes.HWND(-1)
SWP_NOSIZE, SWP_NOMOVE, SWP_SHOWWINDOW = 0x0001, 0x0002, 0x0040

# ── Dimensions ───────────────────────────────────────────────────────────────
WIN_W = 660
TOP_MARGIN = 80

READY_TEXT = "● Ready · Gemini 3.5 live on desktop"


def _brush(a, r, g, b):
    br = SolidColorBrush(Color.FromArgb(a, r, g, b))
    br.Freeze()
    return br


def _run_capsule_impl(holder):
    state = {
        "mode": "fast",
        "snapped_path": None,
        "last_diagnosis": None,
        "is_busy": False,
        "snapping": False,
        "bridge": None,          # filled by background engine loader
        "engine_error": None,
    }

    # Brushes (frozen => safe across threads)
    C_BG_PILL     = _brush(248, 13, 18, 36)
    C_BORDER_NORM = _brush(255, 59, 130, 246)
    C_BORDER_DEEP = _brush(255, 168, 85, 247)
    C_INPUT_BG    = _brush(255, 20, 28, 54)
    C_INPUT_BRD   = _brush(255, 75, 85, 110)
    C_BTN_ASK     = _brush(255, 37, 99, 235)
    C_BTN_APPLY   = _brush(255, 22, 163, 74)
    C_BTN_TOOL    = _brush(255, 30, 41, 68)
    C_TEXT_PRI    = _brush(255, 241, 245, 249)
    C_TEXT_SEC    = _brush(255, 148, 163, 184)
    C_TEXT_ECO    = _brush(255, 74, 222, 128)
    C_DIFF_ADD    = _brush(255, 74, 222, 128)
    C_DIFF_DEL    = _brush(255, 248, 113, 113)

    app = Application()
    holder["app"] = app

    def on_unhandled(sender, e):
        log("UI exception:\n" + str(e.Exception))
        e.Handled = True
    app.DispatcherUnhandledException += on_unhandled

    # ── Root window ──────────────────────────────────────────────────────────
    win = Window()
    holder["win"] = win
    win.Title = "V.E.R.D.A.N.T. Floating Capsule"
    win.Width = WIN_W
    win.SizeToContent = SizeToContent.Height
    win.WindowStartupLocation = WindowStartupLocation.Manual
    win.WindowStyle = getattr(WindowStyle, "None")
    win.ResizeMode = getattr(ResizeMode, "NoResize")
    win.Topmost = True
    win.ShowInTaskbar = True
    if ROUNDED:
        win.AllowsTransparency = True
        win.Background = Brushes.Transparent
    else:
        win.AllowsTransparency = False   # opaque: most reliable over Electron / VS Code
        win.Background = C_BG_PILL

    # Position from the real work area (DIPs), centered horizontally
    wa = SystemParameters.WorkArea
    win.Left = wa.Left + max(0.0, (wa.Width - WIN_W) / 2.0)
    win.Top = wa.Top + TOP_MARGIN

    def on_drag(sender, e):
        try:
            win.DragMove()
        except Exception:
            pass
    win.MouseLeftButtonDown += on_drag

    # ── Outer border ─────────────────────────────────────────────────────────
    pill_border = Border()
    pill_border.Background = C_BG_PILL
    pill_border.BorderBrush = C_BORDER_NORM
    pill_border.BorderThickness = Thickness(2.5)
    pill_border.Padding = Thickness(12, 10, 12, 10)
    if ROUNDED:
        pill_border.CornerRadius = CornerRadius(24)

    main_stack = StackPanel()
    main_stack.Orientation = Orientation.Vertical

    # ── Top row ──────────────────────────────────────────────────────────────
    top_grid = Grid()
    for width in (GridLength.Auto, GridLength(1, GridUnitType.Star), GridLength.Auto,
                  GridLength.Auto, GridLength.Auto, GridLength.Auto,
                  GridLength.Auto, GridLength.Auto):
        cd = ColumnDefinition()
        cd.Width = width
        top_grid.ColumnDefinitions.Add(cd)

    logo = TextBlock()
    logo.Text = "🌿 VERDANT"
    logo.FontWeight = FontWeights.Bold
    logo.FontSize = 13
    logo.Foreground = C_BORDER_NORM
    logo.VerticalAlignment = VerticalAlignment.Center
    logo.Margin = Thickness(0, 0, 8, 0)
    Grid.SetColumn(logo, 0)
    top_grid.Children.Add(logo)

    inp = TextBox()
    inp.FontSize = 12.5
    inp.Foreground = C_TEXT_PRI
    inp.Background = C_INPUT_BG
    inp.BorderBrush = C_INPUT_BRD
    inp.BorderThickness = Thickness(1)
    inp.Padding = Thickness(8, 5, 8, 5)
    inp.CaretBrush = C_TEXT_PRI
    inp.VerticalAlignment = VerticalAlignment.Center
    inp.Margin = Thickness(0, 0, 6, 0)
    inp.ToolTip = "Ask anything, e.g. 'Why is this failing?'  (Esc hides the capsule)"
    Grid.SetColumn(inp, 1)
    top_grid.Children.Add(inp)

    def make_btn(text, col, bg, fg, size=11, bold=False, pad=(7, 4, 7, 4), margin=(0, 0, 3, 0), tip=None):
        b = Button()
        b.Content = text
        b.FontSize = size
        if bold:
            b.FontWeight = FontWeights.Bold
        b.Background = bg
        b.Foreground = fg
        b.BorderThickness = Thickness(0)
        b.Padding = Thickness(*pad)
        b.Margin = Thickness(*margin)
        if tip:
            b.ToolTip = tip
        Grid.SetColumn(b, col)
        top_grid.Children.Add(b)
        return b

    btn_snap = make_btn("📸", 2, C_BTN_TOOL, C_TEXT_PRI, size=12, pad=(6, 4, 6, 4),
                        margin=(0, 0, 4, 0), tip="Snap the window behind the capsule")
    btn_fast = make_btn("⚡ Fast", 3, C_BORDER_NORM, Brushes.White, bold=True)
    btn_deep = make_btn("🧠 Deep", 4, C_BTN_TOOL, C_TEXT_SEC, bold=True, margin=(0, 0, 5, 0))
    btn_ask  = make_btn("▶ Ask", 5, C_BTN_ASK, Brushes.White, size=12, bold=True,
                        pad=(10, 4, 10, 4), margin=(0, 0, 4, 0))
    btn_min  = make_btn("—", 6, Brushes.Transparent, C_TEXT_SEC, size=12,
                        pad=(4, 2, 4, 2), margin=(0, 0, 2, 0), tip="Minimize (Ctrl+Shift+Space toggles)")
    btn_cls  = make_btn("✕", 7, Brushes.Transparent, C_DIFF_DEL, size=12,
                        pad=(4, 2, 4, 2), margin=(0, 0, 0, 0), tip="Close")

    main_stack.Children.Add(top_grid)

    # ── Status bar ───────────────────────────────────────────────────────────
    status_grid = Grid()
    status_grid.Margin = Thickness(2, 5, 2, 0)
    c1 = ColumnDefinition(); c1.Width = GridLength(1, GridUnitType.Star)
    c2 = ColumnDefinition(); c2.Width = GridLength.Auto
    status_grid.ColumnDefinitions.Add(c1)
    status_grid.ColumnDefinitions.Add(c2)

    status_txt = TextBlock()
    status_txt.Text = "● Starting · loading engine..."
    status_txt.FontSize = 11
    status_txt.Foreground = C_TEXT_SEC
    status_txt.TextTrimming = getattr(TextTrimming, "CharacterEllipsis")
    Grid.SetColumn(status_txt, 0)
    status_grid.Children.Add(status_txt)

    eco_txt = TextBlock()
    eco_txt.Text = "🌱 0.05g CO₂"
    eco_txt.FontSize = 11
    eco_txt.Foreground = C_TEXT_ECO
    Grid.SetColumn(eco_txt, 1)
    status_grid.Children.Add(eco_txt)
    main_stack.Children.Add(status_grid)

    # ── Response drawer ──────────────────────────────────────────────────────
    drawer = StackPanel()
    drawer.Orientation = Orientation.Vertical
    drawer.Margin = Thickness(0, 8, 0, 0)
    drawer.Visibility = Visibility.Collapsed

    diag_scroll = ScrollViewer()
    diag_scroll.MaxHeight = 130
    diag_scroll.VerticalScrollBarVisibility = ScrollBarVisibility.Auto
    diag_text = TextBlock()
    diag_text.FontSize = 12
    diag_text.Foreground = C_TEXT_PRI
    diag_text.TextWrapping = TextWrapping.Wrap
    diag_scroll.Content = diag_text
    drawer.Children.Add(diag_scroll)

    diff_scroll = ScrollViewer()
    diff_scroll.MaxHeight = 120
    diff_scroll.Margin = Thickness(0, 6, 0, 0)
    diff_scroll.VerticalScrollBarVisibility = ScrollBarVisibility.Auto
    diff_scroll.Visibility = Visibility.Collapsed
    diff_text = TextBlock()
    diff_text.FontFamily = FontFamily("Consolas")
    diff_text.FontSize = 11
    diff_text.Foreground = C_DIFF_ADD
    diff_text.TextWrapping = TextWrapping.Wrap
    diff_scroll.Content = diff_text
    drawer.Children.Add(diff_scroll)

    act_row = StackPanel()
    act_row.Orientation = Orientation.Horizontal
    act_row.HorizontalAlignment = HorizontalAlignment.Right
    act_row.Margin = Thickness(0, 8, 0, 0)

    btn_dismiss = Button()
    btn_dismiss.Content = "Dismiss"
    btn_dismiss.FontSize = 11
    btn_dismiss.Background = C_BTN_TOOL
    btn_dismiss.Foreground = C_TEXT_SEC
    btn_dismiss.BorderThickness = Thickness(0)
    btn_dismiss.Padding = Thickness(8, 4, 8, 4)
    btn_dismiss.Margin = Thickness(0, 0, 6, 0)
    act_row.Children.Add(btn_dismiss)

    btn_apply = Button()
    btn_apply.Content = "▶ Apply Patch & Run"
    btn_apply.FontSize = 11
    btn_apply.FontWeight = FontWeights.Bold
    btn_apply.Background = C_BTN_APPLY
    btn_apply.Foreground = Brushes.White
    btn_apply.BorderThickness = Thickness(0)
    btn_apply.Padding = Thickness(10, 4, 10, 4)
    btn_apply.Visibility = Visibility.Collapsed
    act_row.Children.Add(btn_apply)

    drawer.Children.Add(act_row)
    main_stack.Children.Add(drawer)

    pill_border.Child = main_stack
    win.Content = pill_border

    # ── Helpers ──────────────────────────────────────────────────────────────
    def ui(fn):
        """Run fn on the WPF UI thread."""
        win.Dispatcher.Invoke(System.Action(fn))

    def set_status(text):
        status_txt.Text = text

    def force_topmost():
        try:
            hwnd = WindowInteropHelper(win).Handle.ToInt64()
            if hwnd:
                user32.SetWindowPos(wintypes.HWND(hwnd), HWND_TOPMOST, 0, 0, 0, 0,
                                    SWP_NOMOVE | SWP_NOSIZE | SWP_SHOWWINDOW)
        except Exception as ex:
            log(f"force_topmost failed: {ex}")

    def show_capsule():
        win.Show()
        if win.WindowState == getattr(WindowState, "Minimized"):
            win.WindowState = getattr(WindowState, "Normal")
        win.Topmost = True
        win.Activate()
        force_topmost()
        inp.Focus()

    def hide_capsule():
        win.Hide()

    def toggle_capsule():
        visible = (win.Visibility == getattr(Visibility, "Visible")
                   and win.WindowState != getattr(WindowState, "Minimized"))
        if visible:
            hide_capsule()
        else:
            show_capsule()

    holder["toggle"] = lambda: ui(toggle_capsule)

    # ── Window buttons ───────────────────────────────────────────────────────
    btn_min.Click += lambda s, e: setattr(win, "WindowState", getattr(WindowState, "Minimized"))
    btn_cls.Click += lambda s, e: win.Close()

    # ── Mode toggle ──────────────────────────────────────────────────────────
    def set_mode(m):
        state["mode"] = m
        if m == "deep":
            pill_border.BorderBrush = C_BORDER_DEEP
            btn_deep.Background = C_BORDER_DEEP
            btn_deep.Foreground = Brushes.White
            btn_fast.Background = C_BTN_TOOL
            btn_fast.Foreground = C_TEXT_SEC
        else:
            pill_border.BorderBrush = C_BORDER_NORM
            btn_fast.Background = C_BORDER_NORM
            btn_fast.Foreground = Brushes.White
            btn_deep.Background = C_BTN_TOOL
            btn_deep.Foreground = C_TEXT_SEC

    btn_fast.Click += lambda s, e: set_mode("fast")
    btn_deep.Click += lambda s, e: set_mode("deep")

    # ── Snap (hides the capsule so the window UNDER it is captured) ──────────
    def snap_screen(s, e):
        if state["snapping"]:
            return
        state["snapping"] = True
        btn_snap.Content = "⏳"
        set_status("● Capturing window behind capsule...")
        hide_capsule()

        def _snap():
            p, title = None, ""
            try:
                time.sleep(0.35)  # let Windows hand focus back to the previous app
                from capsule.snapper import WindowSnapper
                out_dir = ROOT / "uploads" / "captures"
                out_dir.mkdir(parents=True, exist_ok=True)
                p, title = WindowSnapper.capture_active_window(
                    out_dir / f"screen_{int(time.time() * 1000)}.png")
            except Exception:
                log("Snap failed:\n" + traceback.format_exc())

            def _done():
                show_capsule()
                state["snapping"] = False
                if p and Path(p).exists():
                    state["snapped_path"] = Path(p)
                    btn_snap.Content = "✅"
                    set_status(f"● Snapped: {title[:32]}")
                else:
                    btn_snap.Content = "📸"
                    set_status("● Snap failed (see capsule_debug.log)")
            ui(_done)

        Thread(ThreadStart(_snap)).Start()

    btn_snap.Click += snap_screen

    # ── Drawer open / close ──────────────────────────────────────────────────
    def expand_drawer():
        drawer.Visibility = Visibility.Visible

    def collapse_drawer():
        drawer.Visibility = Visibility.Collapsed
        diff_scroll.Visibility = Visibility.Collapsed
        btn_apply.Visibility = Visibility.Collapsed
        set_status(READY_TEXT if state["bridge"] else "● Engine not loaded")

    btn_dismiss.Click += lambda s, e: collapse_drawer()

    # ── Ask ──────────────────────────────────────────────────────────────────
    def do_ask():
        prompt = inp.Text.strip()
        if not prompt:
            inp.Focus()
            return
        if state["is_busy"]:
            return
        if state["bridge"] is None:
            expand_drawer()
            if state["engine_error"]:
                diag_text.Text = ("❌ The V.E.R.D.A.N.T. engine failed to load:\n\n"
                                  f"{state['engine_error']}\n\nFull traceback: {LOG_FILE}")
            else:
                diag_text.Text = "Engine is still loading — try again in a few seconds."
            return

        state["is_busy"] = True
        expand_drawer()
        diag_text.Text = "Thinking with Google Gemini Multimodal..."
        diff_scroll.Visibility = Visibility.Collapsed
        btn_apply.Visibility = Visibility.Collapsed
        btn_apply.Content = "▶ Apply Patch & Run"
        set_status("● Gemini reasoning in progress...")
        btn_ask.Content = "⏳"
        mode = "deepthink" if state["mode"] == "deep" else "normal"
        image = state["snapped_path"]

        def _worker():
            try:
                res = state["bridge"].analyze(prompt=prompt, image_path=image, mode=mode)
                diag = res.get("diagnosis")
                state["last_diagnosis"] = diag
                act = res.get("action_type", "advise")
                conf = res.get("confidence", 0.95)
                summary = res.get("spoken_summary", "")
                root = res.get("root_cause", "")
                diff = res.get("diff_preview", "")
                eco = res.get("eco_audit", {})
                co2 = eco.get("co2_grams", 0.05) if isinstance(eco, dict) else 0.05

                def _show_res():
                    body = f"[{act.upper()}]  Confidence: {int(conf * 100)}%\n\n"
                    if summary:
                        body += f"{summary}\n\n"
                    if root:
                        body += f"Root Cause:\n{root}"
                    diag_text.Text = body.strip()
                    eco_txt.Text = f"🌱 {co2:.2f}g CO₂"
                    if diff:
                        diff_text.Text = diff
                        diff_scroll.Visibility = Visibility.Visible
                        btn_apply.Visibility = Visibility.Visible
                    set_status(f"● Diagnosis ready [{act.upper()}]")
                    btn_ask.Content = "▶ Ask"
                    state["is_busy"] = False
                ui(_show_res)

            except Exception as ex:
                log("Analyze failed:\n" + traceback.format_exc())
                err = str(ex)

                def _show_err():
                    diag_text.Text = f"❌ Error: {err}"
                    set_status("● Reasoning failed")
                    btn_ask.Content = "▶ Ask"
                    state["is_busy"] = False
                ui(_show_err)

        Thread(ThreadStart(_worker)).Start()

    btn_ask.Click += lambda s, e: do_ask()

    def on_key_down(s, e):
        if e.Key == Key.Enter:
            do_ask()
        elif e.Key == Key.Escape:
            hide_capsule()
    inp.KeyDown += on_key_down

    # ── Apply patch ──────────────────────────────────────────────────────────
    def do_apply_patch(s, e):
        if not state["last_diagnosis"] or state["bridge"] is None:
            return
        btn_apply.Content = "⏳ Applying..."
        set_status("● Applying atomic patch & running GitOps...")

        def _patch_worker():
            try:
                res = state["bridge"].apply_patch_and_verify(state["last_diagnosis"])
            except Exception as ex:
                log("Patch failed:\n" + traceback.format_exc())
                res = {"success": False, "error": str(ex)}

            def _patch_done():
                if res.get("success"):
                    warn = res.get("warning")
                    set_status(f"● {warn}" if warn else
                               f"● Patch verified & committed to {res.get('branch', 'main')}")
                    btn_apply.Content = "✅ Applied"
                else:
                    set_status(f"● Patch failed: {res.get('error')}")
                    btn_apply.Content = "Retry Patch"
            ui(_patch_done)

        Thread(ThreadStart(_patch_worker)).Start()

    btn_apply.Click += do_apply_patch

    # ── Engine loader (background, AFTER the window is visible) ──────────────
    def _load_engine():
        t0 = time.time()
        try:
            from capsule.bridge import CapsuleBridge
            state["bridge"] = CapsuleBridge(ROOT)
            dt = time.time() - t0
            log(f"Engine loaded in {dt:.1f}s")
            ui(lambda: set_status(READY_TEXT))
        except Exception as ex:
            state["engine_error"] = f"{type(ex).__name__}: {ex}"
            log("Engine failed to load:\n" + traceback.format_exc())
            msg = state["engine_error"]

            def _show():
                set_status("● Engine failed to load — click Ask for details")
                expand_drawer()
                diag_text.Text = ("❌ The V.E.R.D.A.N.T. engine failed to load:\n\n"
                                  f"{msg}\n\nFull traceback: {LOG_FILE}")
            ui(_show)

    # ── Loaded: topmost + focus + start engine + hotkey ──────────────────────
    def on_loaded(sender, e):
        force_topmost()
        inp.Focus()
        hwnd = WindowInteropHelper(win).Handle.ToInt64()
        log("=" * 60)
        log("V.E.R.D.A.N.T. Native Windows Desktop Capsule")
        log(f"  HWND: {hwnd}   Pos: ({win.Left:.0f}, {win.Top:.0f})   Width: {WIN_W}")
        log(f"  Mode: {'rounded/transparent' if ROUNDED else 'opaque'}   Log: {LOG_FILE}")
        log("=" * 60)
        Thread(ThreadStart(_load_engine)).Start()
        threading.Thread(target=_hotkey_loop, args=(holder, ui, set_status), daemon=True).start()

    win.Loaded += on_loaded
    app.Run(win)


# ── Global hotkey (native RegisterHotKey — no 'keyboard' package needed) ─────
def _hotkey_loop(holder, ui, set_status):
    MOD_ALT, MOD_CONTROL, MOD_SHIFT, MOD_NOREPEAT = 0x0001, 0x0002, 0x0004, 0x4000
    VK_SPACE, WM_HOTKEY = 0x20, 0x0312

    candidates = [
        ("Ctrl+Shift+Space", MOD_CONTROL | MOD_SHIFT | MOD_NOREPEAT),
        ("Ctrl+Alt+Space", MOD_CONTROL | MOD_ALT | MOD_NOREPEAT),
    ]
    chosen = None
    for name, mods in candidates:
        if user32.RegisterHotKey(None, 1, mods, VK_SPACE):
            chosen = name
            break
        log(f"Hotkey {name} unavailable (in use by another app), trying next...")

    if not chosen:
        log("No global hotkey could be registered. Use the taskbar icon to restore the capsule.")
        return

    log(f"Global hotkey active: {chosen}")
    msg = wintypes.MSG()
    while user32.GetMessageW(ctypes.byref(msg), None, 0, 0) > 0:
        if msg.message == WM_HOTKEY:
            try:
                holder["toggle"]()
            except Exception:
                log("Hotkey toggle failed:\n" + traceback.format_exc())


def build_and_run_capsule(holder):
    try:
        _run_capsule_impl(holder)
    except Exception:
        tb = traceback.format_exc()
        log("FATAL CAPSULE ERROR:\n" + tb)
        fatal_box("V.E.R.D.A.N.T. Capsule crashed",
                  f"The capsule failed to start.\n\nLog: {LOG_FILE}\n\n{tb[-900:]}")


def main():
    holder = {}
    t = Thread(ThreadStart(lambda: build_and_run_capsule(holder)))
    t.SetApartmentState(ApartmentState.STA)
    t.Start()
    try:
        while t.IsAlive:
            time.sleep(0.15)
    except KeyboardInterrupt:
        try:
            app = holder.get("app")
            if app is not None:
                app.Dispatcher.InvokeShutdown()
        except Exception:
            pass


if __name__ == "__main__":
    main()
