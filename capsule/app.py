"""
V.E.R.D.A.N.T. v2 — Native Floating AI Desktop Capsule (Tkinter)
Ultra-lightweight, zero external C#/WPF dependencies, 100% pure Python.
Frameless, always-on-top, draggable anywhere on Windows.
Wired live to Google Gemini Multimodal Engine and Atomic Patcher.

Usage:
    python capsule/app.py
"""
import os
import sys
import time
import threading
import traceback
import tkinter as tk
from tkinter import font as tkfont
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

# Load .env
env_file = ROOT / ".env"
if env_file.exists():
    for line in env_file.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and "=" in line and not line.startswith("#"):
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


class FloatingAICapsule:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("V.E.R.D.A.N.T. Floating Capsule")
        self.root.overrideredirect(True)       # Frameless window
        self.root.attributes("-topmost", True)  # Always stay on top of IDE/browser
        
        # Color Palette
        self.BG_DARK = "#0d1224"
        self.BG_CARD = "#141c36"
        self.BG_INPUT = "#1a2444"
        self.BORDER_FAST = "#3b82f6"
        self.BORDER_DEEP = "#a855f7"
        self.TEXT_PRI = "#f8fafc"
        self.TEXT_SEC = "#94a3b8"
        self.TEXT_GREEN = "#22c55e"
        self.TEXT_RED = "#ef4444"
        self.BTN_BLUE = "#2563eb"
        self.BTN_TOOL = "#1e2942"
        self.BTN_APPLY = "#16a34a"

        self.root.configure(bg=self.BG_DARK)

        # State
        self.mode = "fast"
        self.expanded = False
        self.is_busy = False
        self.drag_x = 0
        self.drag_y = 0
        self.snapped_path = None
        self.bridge = None
        self.engine_error = None
        self.last_diagnosis = None

        self.build_ui()
        self.bind_events()
        self.position_top_center()

        # Start asynchronous engine initialization
        threading.Thread(target=self._load_engine_async, daemon=True).start()

    def build_ui(self):
        # Outer Border
        self.container = tk.Frame(
            self.root, bg=self.BG_DARK,
            highlightbackground=self.BORDER_FAST,
            highlightthickness=2, padx=10, pady=8
        )
        self.container.pack(fill="both", expand=True)

        # ── Top Pill Bar ─────────────────────────────────────────────────────
        self.pill_bar = tk.Frame(self.container, bg=self.BG_DARK)
        self.pill_bar.pack(fill="x")

        # Logo
        self.logo = tk.Label(
            self.pill_bar, text="🌿 VERDANT", fg=self.BORDER_FAST,
            bg=self.BG_DARK, font=("Segoe UI", 10, "bold"), cursor="hand2"
        )
        self.logo.pack(side="left", padx=(0, 8))

        # Text Input
        self.entry = tk.Entry(
            self.pill_bar, bg=self.BG_INPUT, fg=self.TEXT_PRI,
            insertbackground=self.BORDER_FAST, bd=0,
            font=("Segoe UI", 10), width=32
        )
        self.entry.pack(side="left", fill="x", expand=True, ipady=4, padx=(0, 6))
        self.entry.bind("<Return>", lambda e: self.do_ask())

        # Snap Button
        self.btn_snap = tk.Button(
            self.pill_bar, text="📸", bg=self.BTN_TOOL, fg=self.TEXT_PRI,
            activebackground=self.BG_INPUT, activeforeground="#ffffff",
            bd=0, font=("Segoe UI", 10), cursor="hand2", padx=6, pady=2,
            command=self.do_snap
        )
        self.btn_snap.pack(side="left", padx=(0, 4))

        # Fast Mode Button
        self.btn_fast = tk.Button(
            self.pill_bar, text="⚡ Fast", bg=self.BORDER_FAST, fg="#ffffff",
            activebackground=self.BORDER_FAST, activeforeground="#ffffff",
            bd=0, font=("Segoe UI", 9, "bold"), cursor="hand2", padx=7, pady=2,
            command=lambda: self.set_mode("fast")
        )
        self.btn_fast.pack(side="left", padx=(0, 2))

        # Deep Mode Button
        self.btn_deep = tk.Button(
            self.pill_bar, text="🧠 Deep", bg=self.BTN_TOOL, fg=self.TEXT_SEC,
            activebackground=self.BORDER_DEEP, activeforeground="#ffffff",
            bd=0, font=("Segoe UI", 9, "bold"), cursor="hand2", padx=7, pady=2,
            command=lambda: self.set_mode("deep")
        )
        self.btn_deep.pack(side="left", padx=(0, 4))

        # Ask Button
        self.btn_ask = tk.Button(
            self.pill_bar, text="▶ Ask", bg=self.BTN_BLUE, fg="#ffffff",
            activebackground="#1d4ed8", activeforeground="#ffffff",
            bd=0, font=("Segoe UI", 9, "bold"), cursor="hand2", padx=10, pady=2,
            command=self.do_ask
        )
        self.btn_ask.pack(side="left", padx=(0, 4))

        # Close Button
        self.btn_close = tk.Label(
            self.pill_bar, text="✕", fg=self.TEXT_RED, bg=self.BG_DARK,
            font=("Segoe UI", 10, "bold"), cursor="hand2"
        )
        self.btn_close.pack(side="right", padx=(2, 0))
        self.btn_close.bind("<Button-1>", lambda e: self.root.destroy())

        # ── Status Row ───────────────────────────────────────────────────────
        self.status_bar = tk.Frame(self.container, bg=self.BG_DARK)
        self.status_bar.pack(fill="x", pady=(4, 0))

        self.status_lbl = tk.Label(
            self.status_bar, text="● Starting · loading engine...",
            fg=self.TEXT_SEC, bg=self.BG_DARK, font=("Segoe UI", 8)
        )
        self.status_lbl.pack(side="left")

        self.eco_lbl = tk.Label(
            self.status_bar, text="🌱 0.05g CO₂",
            fg=self.TEXT_GREEN, bg=self.BG_DARK, font=("Segoe UI", 8, "bold")
        )
        self.eco_lbl.pack(side="right")

        # ── Expandable Response Drawer (Hidden by default) ───────────────────
        self.drawer = tk.Frame(self.container, bg=self.BG_DARK)

        # Diagnosis Log
        self.diag_box = tk.Text(
            self.drawer, height=6, bg="#090d1a", fg=self.TEXT_PRI,
            bd=0, padx=8, pady=6, wrap="word", font=("Segoe UI", 9), state="disabled"
        )
        self.diag_box.pack(fill="x", pady=(8, 4))

        # Diff View Frame (Hidden unless diff exists)
        self.diff_frame = tk.Frame(self.drawer, bg=self.BG_DARK)
        self.diff_box = tk.Text(
            self.diff_frame, height=6, bg="#070a14", fg=self.TEXT_GREEN,
            bd=0, padx=8, pady=6, wrap="none", font=("Consolas", 9), state="disabled"
        )
        self.diff_box.pack(fill="x", pady=(0, 4))

        # Action Buttons Row
        self.action_row = tk.Frame(self.drawer, bg=self.BG_DARK)
        self.action_row.pack(fill="x", pady=(4, 0))

        self.btn_dismiss = tk.Button(
            self.action_row, text="Dismiss", bg=self.BTN_TOOL, fg=self.TEXT_SEC,
            bd=0, font=("Segoe UI", 8), cursor="hand2", padx=8, pady=2,
            command=self.collapse_drawer
        )
        self.btn_dismiss.pack(side="right", padx=(6, 0))

        self.btn_apply = tk.Button(
            self.action_row, text="▶ Apply Patch & Run", bg=self.BTN_APPLY, fg="#ffffff",
            bd=0, font=("Segoe UI", 8, "bold"), cursor="hand2", padx=10, pady=2,
            command=self.do_apply_patch
        )
        # Hidden until diff ready

    def bind_events(self):
        # Dragging on frames and labels
        drag_targets = [self.container, self.pill_bar, self.logo, self.status_bar, self.status_lbl, self.eco_lbl]
        for w in drag_targets:
            w.bind("<ButtonPress-1>", self.start_drag)
            w.bind("<B1-Motion>", self.do_drag)

        self.root.bind("<Escape>", lambda e: self.collapse_drawer())

    def position_top_center(self):
        self.root.update_idletasks()
        w = 660
        h = max(74, self.root.winfo_reqheight())
        sw = self.root.winfo_screenwidth()
        x = max(20, (sw - w) // 2)
        y = 70
        self.root.geometry(f"{w}x{h}+{x}+{y}")

    def start_drag(self, event):
        self.drag_x = event.x
        self.drag_y = event.y

    def do_drag(self, event):
        x = self.root.winfo_x() + (event.x - self.drag_x)
        y = self.root.winfo_y() + (event.y - self.drag_y)
        self.root.geometry(f"+{x}+{y}")

    def set_mode(self, mode):
        self.mode = mode
        if mode == "deep":
            self.container.configure(highlightbackground=self.BORDER_DEEP)
            self.btn_deep.configure(bg=self.BORDER_DEEP, fg="#ffffff")
            self.btn_fast.configure(bg=self.BTN_TOOL, fg=self.TEXT_SEC)
            self.logo.configure(fg=self.BORDER_DEEP)
        else:
            self.container.configure(highlightbackground=self.BORDER_FAST)
            self.btn_fast.configure(bg=self.BORDER_FAST, fg="#ffffff")
            self.btn_deep.configure(bg=self.BTN_TOOL, fg=self.TEXT_SEC)
            self.logo.configure(fg=self.BORDER_FAST)

    def set_status(self, text):
        self.status_lbl.configure(text=text)

    def expand_drawer(self):
        if not self.expanded:
            self.expanded = True
            self.drawer.pack(fill="x", pady=(4, 0))
            self.root.update_idletasks()
            self.root.geometry("")

    def collapse_drawer(self):
        if self.expanded:
            self.expanded = False
            self.drawer.pack_forget()
            self.diff_frame.pack_forget()
            self.btn_apply.pack_forget()
            self.set_status("● Ready · Gemini 3.5 live on desktop" if self.bridge else "● Engine not loaded")
            self.root.update_idletasks()
            self.root.geometry("")

    def _load_engine_async(self):
        try:
            from capsule.bridge import CapsuleBridge
            self.bridge = CapsuleBridge(ROOT)
            self.root.after(0, lambda: self.set_status("● Ready · Gemini 3.5 live on desktop"))
        except Exception as e:
            self.engine_error = str(e)
            self.root.after(0, lambda: self.set_status(f"● Engine load error: {e}"))

    def do_snap(self):
        self.btn_snap.configure(text="⏳")
        self.set_status("● Capturing window behind capsule...")
        
        # Hide capsule temporarily so underlying app is captured
        self.root.withdraw()

        def _worker():
            p, title = None, ""
            try:
                time.sleep(0.35)
                from capsule.snapper import WindowSnapper
                out_dir = ROOT / "uploads" / "captures"
                out_dir.mkdir(parents=True, exist_ok=True)
                p, title = WindowSnapper.capture_active_window(
                    out_dir / f"screen_{int(time.time() * 1000)}.png"
                )
            except Exception as e:
                print(f"[Snap Error] {e}")

            def _done():
                self.root.deiconify()
                if p and Path(p).exists():
                    self.snapped_path = Path(p)
                    self.btn_snap.configure(text="✅")
                    self.set_status(f"● Snapped: {title[:32]}")
                else:
                    self.btn_snap.configure(text="📸")
                    self.set_status("● Snap failed")

            self.root.after(0, _done)

        threading.Thread(target=_worker, daemon=True).start()

    def do_ask(self):
        prompt = self.entry.get().strip()
        if not prompt or self.is_busy:
            return
        
        if self.bridge is None:
            self.expand_drawer()
            self.diag_box.configure(state="normal")
            self.diag_box.delete("1.0", "end")
            self.diag_box.insert("end", f"❌ Engine not loaded:\n{self.engine_error or 'Still initializing...'}")
            self.diag_box.configure(state="disabled")
            return

        self.is_busy = True
        self.btn_ask.configure(text="⏳")
        self.set_status("● Gemini reasoning in progress...")
        self.expand_drawer()

        self.diag_box.configure(state="normal")
        self.diag_box.delete("1.0", "end")
        self.diag_box.insert("end", "Analyzing with Google Gemini Multimodal Engine...")
        self.diag_box.configure(state="disabled")
        self.diff_frame.pack_forget()
        self.btn_apply.pack_forget()

        def _worker():
            try:
                mode = "deepthink" if self.mode == "deep" else "normal"
                res = self.bridge.analyze(prompt=prompt, image_path=self.snapped_path, mode=mode)
                self.last_diagnosis = res.get("diagnosis")
                act = res.get("action_type", "advise")
                conf = res.get("confidence", 0.95)
                summary = res.get("spoken_summary", "")
                root = res.get("root_cause", "")
                diff = res.get("diff_preview", "")
                eco = res.get("eco_audit", {})
                co2 = eco.get("co2_grams", 0.05) if isinstance(eco, dict) else 0.05

                def _ui_update():
                    self.diag_box.configure(state="normal")
                    self.diag_box.delete("1.0", "end")
                    msg = f"[{act.upper()}] Confidence: {int(conf * 100)}%\n\n"
                    if summary:
                        msg += f"{summary}\n\n"
                    if root:
                        msg += f"Root Cause:\n{root}"
                    self.diag_box.insert("end", msg.strip())
                    self.diag_box.configure(state="disabled")

                    self.eco_lbl.configure(text=f"🌱 {co2:.2f}g CO₂")

                    if diff:
                        self.diff_box.configure(state="normal")
                        self.diff_box.delete("1.0", "end")
                        self.diff_box.insert("end", diff)
                        self.diff_box.configure(state="disabled")
                        self.diff_frame.pack(fill="x", pady=(0, 4))
                        self.btn_apply.pack(side="right", padx=(0, 6))

                    self.set_status(f"● Diagnosis ready [{act.upper()}]")
                    self.btn_ask.configure(text="▶ Ask")
                    self.is_busy = False

                self.root.after(0, _ui_update)

            except Exception as ex:
                err_msg = str(ex)
                def _ui_err():
                    self.diag_box.configure(state="normal")
                    self.diag_box.delete("1.0", "end")
                    self.diag_box.insert("end", f"❌ Error:\n{err_msg}")
                    self.diag_box.configure(state="disabled")
                    self.set_status("● Reasoning failed")
                    self.btn_ask.configure(text="▶ Ask")
                    self.is_busy = False
                self.root.after(0, _ui_err)

        threading.Thread(target=_worker, daemon=True).start()

    def do_apply_patch(self):
        if not self.last_diagnosis or self.bridge is None:
            return
        self.btn_apply.configure(text="⏳ Applying...")
        self.set_status("● Applying patch & verifying GitOps...")

        def _worker():
            try:
                res = self.bridge.apply_patch_and_verify(self.last_diagnosis)
            except Exception as e:
                res = {"success": False, "error": str(e)}

            def _done():
                if res.get("success"):
                    self.btn_apply.configure(text="✅ Applied")
                    self.set_status(f"● Patch verified on {res.get('branch', 'main')}")
                else:
                    self.btn_apply.configure(text="Retry Patch")
                    self.set_status(f"● Patch failed: {res.get('error')}")

            self.root.after(0, _done)

        threading.Thread(target=_worker, daemon=True).start()

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    FloatingAICapsule().run()
