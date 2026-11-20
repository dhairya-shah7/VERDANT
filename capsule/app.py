"""
V.E.R.D.A.N.T. v2 — Native Windows Desktop Floating Capsule
Built with Windows Presentation Foundation (WPF) via pythonnet.
True hardware-accelerated floating pill: frameless, transparent, always on top.

Usage:
    python capsule/app.py
"""
import os
import sys
import time
import json
import threading
from pathlib import Path

# Setup paths and environment
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

# Load .env variables
env_file = ROOT / ".env"
if env_file.exists():
    for line in env_file.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and "=" in line and not line.startswith("#"):
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip())

# Add WPF references
sys.path.append(r"C:\Windows\Microsoft.NET\Framework64\v4.0.30319\WPF")
import clr
clr.AddReference("PresentationFramework")
clr.AddReference("PresentationCore")
clr.AddReference("WindowsBase")

import System
from System.Threading import Thread, ThreadStart, ApartmentState
from System.Windows import (
    Application, Window, WindowStyle, WindowStartupLocation,
    HorizontalAlignment, VerticalAlignment, CornerRadius, Thickness,
    Visibility, TextWrapping, FontWeights
)
from System.Windows.Media import (
    Brushes, Color, SolidColorBrush, FontFamily
)
from System.Windows.Controls import (
    Border, StackPanel, Grid, TextBox, TextBlock, Button, ScrollViewer,
    ColumnDefinition, RowDefinition, GridLength, GridUnitType, Orientation
)

from capsule.bridge import CapsuleBridge
from capsule.snapper import WindowSnapper

# ── Dimensions ───────────────────────────────────────────────────────────────
WIN_W = 660
COLLAPSED_H = 76
EXPANDED_H = 390
WIN_LEFT = (1280 - WIN_W) // 2  # 310
WIN_TOP = 22

# ── Colors ───────────────────────────────────────────────────────────────────
C_BG_PILL    = SolidColorBrush(Color.FromArgb(248, 13, 18, 36))     # Deep dark navy
C_BORDER_NORM= SolidColorBrush(Color.FromArgb(220, 59, 130, 246))   # Neon blue
C_BORDER_DEEP= SolidColorBrush(Color.FromArgb(220, 168, 85, 247))   # Neon purple
C_INPUT_BG   = SolidColorBrush(Color.FromArgb(180, 20, 28, 54))     # Input field dark
C_INPUT_BRD  = SolidColorBrush(Color.FromArgb(100, 255, 255, 255))
C_BTN_ASK    = SolidColorBrush(Color.FromArgb(255, 37, 99, 235))    # Blue accent
C_BTN_APPLY  = SolidColorBrush(Color.FromArgb(255, 22, 163, 74))   # Green
C_BTN_TOOL   = SolidColorBrush(Color.FromArgb(120, 30, 41, 68))
C_TEXT_PRI   = SolidColorBrush(Color.FromArgb(255, 241, 245, 249))
C_TEXT_SEC   = SolidColorBrush(Color.FromArgb(255, 148, 163, 184))
C_TEXT_ECO   = SolidColorBrush(Color.FromArgb(255, 74, 222, 128))
C_DIFF_ADD   = SolidColorBrush(Color.FromArgb(255, 74, 222, 128))
C_DIFF_DEL   = SolidColorBrush(Color.FromArgb(255, 248, 113, 113))


def build_and_run_capsule():
    bridge = CapsuleBridge(ROOT)
    state = {
        "mode": "fast",
        "snapped_path": None,
        "last_diagnosis": None,
        "is_busy": False
    }

    app = Application()

    # ── Root Window ──────────────────────────────────────────────────────────
    win = Window()
    win.Title = "V.E.R.D.A.N.T. Floating Capsule"
    win.Width = WIN_W
    win.Height = COLLAPSED_H
    win.Left = WIN_LEFT
    win.Top = WIN_TOP
    win.WindowStyle = getattr(WindowStyle, "None")
    win.AllowsTransparency = True
    win.Background = Brushes.Transparent
    win.Topmost = True
    win.ShowInTaskbar = True

    # Drag window anywhere
    def on_drag(sender, e):
        try:
            win.DragMove()
        except Exception:
            pass
    win.MouseLeftButtonDown += on_drag

    # ── Outer Pill Border ────────────────────────────────────────────────────
    pill_border = Border()
    pill_border.CornerRadius = CornerRadius(16)
    pill_border.Background = C_BG_PILL
    pill_border.BorderBrush = C_BORDER_NORM
    pill_border.BorderThickness = Thickness(1.8)
    pill_border.Padding = Thickness(10, 8, 10, 8)

    # ── Main Vertical Layout ─────────────────────────────────────────────────
    main_stack = StackPanel()
    main_stack.Orientation = Orientation.Vertical

    # ── Top Row Controls ─────────────────────────────────────────────────────
    top_grid = Grid()
    col_logo = ColumnDefinition(); col_logo.Width = GridLength.Auto
    col_inp  = ColumnDefinition(); col_inp.Width  = GridLength(1, GridUnitType.Star)
    col_snap = ColumnDefinition(); col_snap.Width = GridLength.Auto
    col_fast = ColumnDefinition(); col_fast.Width = GridLength.Auto
    col_deep = ColumnDefinition(); col_deep.Width = GridLength.Auto
    col_ask  = ColumnDefinition(); col_ask.Width  = GridLength.Auto
    col_min  = ColumnDefinition(); col_min.Width  = GridLength.Auto
    col_cls  = ColumnDefinition(); col_cls.Width  = GridLength.Auto

    top_grid.ColumnDefinitions.Add(col_logo)
    top_grid.ColumnDefinitions.Add(col_inp)
    top_grid.ColumnDefinitions.Add(col_snap)
    top_grid.ColumnDefinitions.Add(col_fast)
    top_grid.ColumnDefinitions.Add(col_deep)
    top_grid.ColumnDefinitions.Add(col_ask)
    top_grid.ColumnDefinitions.Add(col_min)
    top_grid.ColumnDefinitions.Add(col_cls)

    # 1. Logo
    logo = TextBlock()
    logo.Text = "🌿 VERDANT"
    logo.FontWeight = FontWeights.Bold
    logo.FontSize = 13
    logo.Foreground = C_BORDER_NORM
    logo.VerticalAlignment = VerticalAlignment.Center
    logo.Margin = Thickness(0, 0, 8, 0)
    Grid.SetColumn(logo, 0)
    top_grid.Children.Add(logo)

    # 2. Input Box
    inp = TextBox()
    inp.FontSize = 12.5
    inp.Foreground = C_TEXT_PRI
    inp.Background = C_INPUT_BG
    inp.BorderBrush = C_INPUT_BRD
    inp.BorderThickness = Thickness(1)
    inp.Padding = Thickness(8, 5, 8, 5)
    inp.VerticalAlignment = VerticalAlignment.Center
    inp.Margin = Thickness(0, 0, 6, 0)
    Grid.SetColumn(inp, 1)
    top_grid.Children.Add(inp)

    # 3. Snap Button
    btn_snap = Button()
    btn_snap.Content = "📸"
    btn_snap.Background = C_BTN_TOOL
    btn_snap.Foreground = C_TEXT_PRI
    btn_snap.BorderThickness = Thickness(0)
    btn_snap.Padding = Thickness(6, 4, 6, 4)
    btn_snap.Margin = Thickness(0, 0, 4, 0)
    btn_snap.ToolTip = "Snap Foreground Window (VS Code, App, Terminal)"
    Grid.SetColumn(btn_snap, 2)
    top_grid.Children.Add(btn_snap)

    # 4. Fast Mode Button
    btn_fast = Button()
    btn_fast.Content = "⚡ Fast"
    btn_fast.FontSize = 11
    btn_fast.FontWeight = FontWeights.SemiBold
    btn_fast.Background = C_BORDER_NORM
    btn_fast.Foreground = Brushes.White
    btn_fast.BorderThickness = Thickness(0)
    btn_fast.Padding = Thickness(7, 4, 7, 4)
    btn_fast.Margin = Thickness(0, 0, 3, 0)
    Grid.SetColumn(btn_fast, 3)
    top_grid.Children.Add(btn_fast)

    # 5. Deep Mode Button
    btn_deep = Button()
    btn_deep.Content = "🧠 Deep"
    btn_deep.FontSize = 11
    btn_deep.FontWeight = FontWeights.SemiBold
    btn_deep.Background = C_BTN_TOOL
    btn_deep.Foreground = C_TEXT_SEC
    btn_deep.BorderThickness = Thickness(0)
    btn_deep.Padding = Thickness(7, 4, 7, 4)
    btn_deep.Margin = Thickness(0, 0, 5, 0)
    Grid.SetColumn(btn_deep, 4)
    top_grid.Children.Add(btn_deep)

    # 6. Ask Button
    btn_ask = Button()
    btn_ask.Content = "▶ Ask"
    btn_ask.FontSize = 12
    btn_ask.FontWeight = FontWeights.Bold
    btn_ask.Background = C_BTN_ASK
    btn_ask.Foreground = Brushes.White
    btn_ask.BorderThickness = Thickness(0)
    btn_ask.Padding = Thickness(10, 4, 10, 4)
    btn_ask.Margin = Thickness(0, 0, 4, 0)
    Grid.SetColumn(btn_ask, 5)
    top_grid.Children.Add(btn_ask)

    # 7. Minimize
    btn_min = Button()
    btn_min.Content = "—"
    btn_min.FontSize = 12
    btn_min.Background = Brushes.Transparent
    btn_min.Foreground = C_TEXT_SEC
    btn_min.BorderThickness = Thickness(0)
    btn_min.Padding = Thickness(4, 2, 4, 2)
    btn_min.Margin = Thickness(0, 0, 2, 0)
    btn_min.Click += lambda s, e: win.set_WindowState(getattr(System.Windows.WindowState, "Minimized"))
    Grid.SetColumn(btn_min, 6)
    top_grid.Children.Add(btn_min)

    # 8. Close
    btn_cls = Button()
    btn_cls.Content = "✕"
    btn_cls.FontSize = 12
    btn_cls.Background = Brushes.Transparent
    btn_cls.Foreground = C_DIFF_DEL
    btn_cls.BorderThickness = Thickness(0)
    btn_cls.Padding = Thickness(4, 2, 4, 2)
    btn_cls.Click += lambda s, e: win.Close()
    Grid.SetColumn(btn_cls, 7)
    top_grid.Children.Add(btn_cls)

    main_stack.Children.Add(top_grid)

    # ── Status Bar ───────────────────────────────────────────────────────────
    status_grid = Grid()
    status_grid.Margin = Thickness(2, 5, 2, 0)
    c1 = ColumnDefinition(); c1.Width = GridLength(1, GridUnitType.Star)
    c2 = ColumnDefinition(); c2.Width = GridLength.Auto
    status_grid.ColumnDefinitions.Add(c1)
    status_grid.ColumnDefinitions.Add(c2)

    status_txt = TextBlock()
    status_txt.Text = "● Ready · Gemini 3.5 live on desktop"
    status_txt.FontSize = 11
    status_txt.Foreground = C_TEXT_SEC
    Grid.SetColumn(status_txt, 0)
    status_grid.Children.Add(status_txt)

    eco_txt = TextBlock()
    eco_txt.Text = "🌱 0.05g CO₂"
    eco_txt.FontSize = 11
    eco_txt.Foreground = C_TEXT_ECO
    Grid.SetColumn(eco_txt, 1)
    status_grid.Children.Add(eco_txt)

    main_stack.Children.Add(status_grid)

    # ── Response Drawer (Collapsed by default) ────────────────────────────────
    drawer = StackPanel()
    drawer.Orientation = Orientation.Vertical
    drawer.Margin = Thickness(0, 8, 0, 0)
    drawer.Visibility = Visibility.Collapsed

    # Diagnosis ScrollBox
    diag_scroll = ScrollViewer()
    diag_scroll.MaxHeight = 130
    diag_scroll.VerticalScrollBarVisibility = getattr(System.Windows.Controls.ScrollBarVisibility, "Auto")

    diag_text = TextBlock()
    diag_text.Text = ""
    diag_text.FontSize = 12
    diag_text.Foreground = C_TEXT_PRI
    diag_text.TextWrapping = TextWrapping.Wrap
    diag_scroll.Content = diag_text
    drawer.Children.Add(diag_scroll)

    # Diff Box
    diff_scroll = ScrollViewer()
    diff_scroll.MaxHeight = 120
    diff_scroll.Margin = Thickness(0, 6, 0, 0)
    diff_scroll.Visibility = Visibility.Collapsed

    diff_text = TextBlock()
    diff_text.FontFamily = FontFamily("Consolas")
    diff_text.FontSize = 11
    diff_text.Foreground = C_DIFF_ADD
    diff_text.TextWrapping = TextWrapping.Wrap
    diff_scroll.Content = diff_text
    drawer.Children.Add(diff_scroll)

    # Drawer Actions (Apply & Dismiss)
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

    # ── Interactive Handlers ─────────────────────────────────────────────────
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

    def snap_screen(s, e):
        btn_snap.Content = "⏳"
        status_txt.Text = "● Capturing active window under capsule..."
        def _snap():
            p, title = WindowSnapper.capture_active_window()
            def _done():
                if p and p.exists():
                    state["snapped_path"] = p
                    btn_snap.Content = "✅"
                    status_txt.Text = f"● Snapped: {title[:32]}"
                else:
                    btn_snap.Content = "📸"
                    status_txt.Text = "● Snap failed"
            win.Dispatcher.Invoke(System.Action(_done))
        threading.Thread(target=_snap, daemon=True).start()

    btn_snap.Click += snap_screen

    def expand_drawer():
        win.Height = EXPANDED_H
        drawer.Visibility = Visibility.Visible

    def collapse_drawer():
        drawer.Visibility = Visibility.Collapsed
        diff_scroll.Visibility = Visibility.Collapsed
        btn_apply.Visibility = Visibility.Collapsed
        win.Height = COLLAPSED_H
        status_txt.Text = "● Ready · Gemini 3.5 live on desktop"

    btn_dismiss.Click += lambda s, e: collapse_drawer()

    def do_ask():
        prompt = inp.Text.strip()
        if not prompt:
            inp.Focus()
            return

        if state["is_busy"]:
            return
        state["is_busy"] = True

        expand_drawer()
        diag_text.Text = "Thinking with Google Gemini Multimodal..."
        diff_scroll.Visibility = Visibility.Collapsed
        btn_apply.Visibility = Visibility.Collapsed
        status_txt.Text = "● Gemini reasoning in progress..."
        btn_ask.Content = "⏳"

        def _worker():
            try:
                res = bridge.analyze(
                    prompt=prompt,
                    image_path=state["snapped_path"],
                    mode="deepthink" if state["mode"] == "deep" else "normal"
                )
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

                    status_txt.Text = f"● Diagnosis ready [{act.upper()}]"
                    btn_ask.Content = "▶ Ask"
                    state["is_busy"] = False

                win.Dispatcher.Invoke(System.Action(_show_res))

            except Exception as ex:
                def _show_err():
                    diag_text.Text = f"❌ Error: {ex}"
                    status_txt.Text = "● Reasoning failed"
                    btn_ask.Content = "▶ Ask"
                    state["is_busy"] = False
                win.Dispatcher.Invoke(System.Action(_show_err))

        threading.Thread(target=_worker, daemon=True).start()

    btn_ask.Click += lambda s, e: do_ask()

    def on_key_down(s, e):
        if e.Key == getattr(System.Windows.Input.Key, "Enter"):
            do_ask()
    inp.KeyDown += on_key_down

    def do_apply_patch(s, e):
        if not state["last_diagnosis"]:
            return
        btn_apply.Content = "⏳ Applying..."
        status_txt.Text = "● Applying atomic patch & running GitOps..."

        def _patch_worker():
            res = bridge.apply_patch_and_verify(state["last_diagnosis"])
            def _patch_done():
                if res.get("success"):
                    status_txt.Text = f"● Patch verified & committed to {res.get('branch', 'main')}"
                    btn_apply.Content = "✅ Applied"
                else:
                    status_txt.Text = f"● Patch failed: {res.get('error')}"
                    btn_apply.Content = "Retry Patch"
            win.Dispatcher.Invoke(System.Action(_patch_done))

        threading.Thread(target=_patch_worker, daemon=True).start()

    btn_apply.Click += do_apply_patch

    print("=" * 60)
    print("🌿 V.E.R.D.A.N.T. Native Windows Desktop Capsule")
    print(f"   WPF Hardware-Accelerated Floating Pill")
    print(f"   Position: ({WIN_LEFT}, {WIN_TOP})  Size: {WIN_W}x{COLLAPSED_H}")
    print("   Always On Top · Frameless · Draggable")
    print("=" * 60)

    app.Run(win)


def main():
    t = Thread(ThreadStart(build_and_run_capsule))
    t.SetApartmentState(ApartmentState.STA)
    t.Start()
    t.Join()


if __name__ == "__main__":
    main()
