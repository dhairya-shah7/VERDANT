"""
V.E.R.D.A.N.T. Desktop Floating Capsule UI (Native High-Performance Tkinter)
100% Native, zero DPI scaling glitches, zero titlebar hijacking:
- Sleek dark theme (#0D111A) with neon glowing perimeter (#3B82F6 / #A855F7)
- Always-on-top floating pill anchored to Windows taskbar
- Text input with '| Ask anything...' placeholder
- Controls: [+] attach active window, [🌿 Normal ▾] vs [💡 DeepThink ▾], [🎙️ Voice] audio, [➤] submit
- Expandable slide-out diff drawer with 1-click apply and proof verification
"""
import threading
from pathlib import Path
from typing import Optional, Dict, Any
import tkinter as tk
from tkinter import font as tkfont

from .snapper import WindowSnapper
from .voice import VoiceRecorder
from .bridge import CapsuleBridge


class FloatingCapsule(tk.Tk):
    def __init__(self):
        super().__init__()

        self.bridge = CapsuleBridge()
        self.voice_recorder = VoiceRecorder()

        # State tracking
        self.active_mode = "Normal"  # "Normal" or "DeepThink"
        self.attached_screenshot: Optional[Path] = None
        self.attached_screenshot_title: Optional[str] = None
        self.recording_voice = False
        self.voice_audio_bytes: Optional[bytes] = None
        self.latest_diagnosis = None
        self.is_drawer_open = False
        self.is_visible = True

        # Window Title & Topmost Floating Behavior
        self.title("🌿 V.E.R.D.A.N.T. Capsule")
        self.attributes("-topmost", True)
        self.configure(bg="#06090F")
        self.resizable(False, False)

        # Precise On-Screen Geometry (Centered in Middle of Screen)
        screen_w = self.winfo_screenwidth() or 1280
        screen_h = self.winfo_screenheight() or 800
        self.capsule_width = 660
        self.capsule_height = 98
        self.drawer_height = 280

        init_x = max(20, int((screen_w - self.capsule_width) / 2))
        init_y = max(40, int((screen_h - self.capsule_height) / 3))
        self.geometry(f"{self.capsule_width}x{self.capsule_height}+{init_x}+{init_y}")

        # Drag Window Handlers
        self._drag_data = {"x": 0, "y": 0}

        self._build_ui()
        self._bind_drag(self.glow_border)
        self._bind_drag(self.main_pill)

        # Ensure Immediate Visibility & Focus
        self.deiconify()
        self.lift()
        self.attributes("-topmost", True)
        self.focus_force()

    def _bind_drag(self, widget):
        widget.bind("<ButtonPress-1>", self._start_drag)
        widget.bind("<B1-Motion>", self._on_drag)

    def _start_drag(self, event):
        self._drag_data["x"] = event.x
        self._drag_data["y"] = event.y

    def _on_drag(self, event):
        x = self.winfo_x() + (event.x - self._drag_data["x"])
        y = self.winfo_y() + (event.y - self._drag_data["y"])
        self.geometry(f"+{x}+{y}")

    def toggle_visibility(self):
        """Toggles show/hide safely on main thread."""
        if self.is_visible:
            self.withdraw()
            self.is_visible = False
        else:
            self.deiconify()
            self.lift()
            self.attributes("-topmost", True)
            self.focus_force()
            self.is_visible = True

    def _build_ui(self):
        # Outer Glowing Frame (Simulates Neon Glow Perimeter)
        self.glow_border = tk.Frame(
            self,
            bg="#3B82F6",
            bd=0,
            highlightthickness=1,
            highlightbackground="#3B82F6"
        )
        self.glow_border.pack(fill="both", expand=True, padx=2, pady=2)

        # Main Capsule Body
        self.main_pill = tk.Frame(
            self.glow_border,
            bg="#0D111A",
            bd=0
        )
        self.main_pill.pack(fill="both", expand=True, padx=1, pady=1)

        # ---------------- TOP ROW: Prompt Input & Snapped Badge ----------------
        self.top_row = tk.Frame(self.main_pill, bg="#0D111A")
        self.top_row.pack(fill="x", padx=12, pady=(8, 2))

        self.input_entry = tk.Entry(
            self.top_row,
            bg="#0D111A",
            fg="#F1F5F9",
            insertbackground="#38BDF8",
            font=("Segoe UI", 12),
            relief="flat",
            bd=0
        )
        self.placeholder_text = "| Ask anything... (e.g. 'Why is this failing?' or 'Fix the order checkout')"
        self.input_entry.insert(0, self.placeholder_text)
        self.input_entry.configure(fg="#64748B")
        self.input_entry.bind("<FocusIn>", self._on_entry_focus_in)
        self.input_entry.bind("<FocusOut>", self._on_entry_focus_out)
        self.input_entry.bind("<Return>", lambda e: self.on_submit())
        self.input_entry.pack(side="left", fill="x", expand=True)

        # Screenshot Thumbnail / Badge (Initially Hidden)
        self.snap_badge = tk.Button(
            self.top_row,
            text="",
            bg="#1E293B",
            fg="#38BDF8",
            activebackground="#334155",
            activeforeground="#38BDF8",
            relief="flat",
            font=("Segoe UI", 9, "bold"),
            bd=0,
            padx=6,
            pady=2,
            command=self.clear_attached_screen
        )

        # ---------------- BOTTOM ROW: Mode, Attachment, Voice, Submit ----------------
        self.bot_row = tk.Frame(self.main_pill, bg="#0D111A")
        self.bot_row.pack(fill="x", padx=12, pady=(4, 8))

        # Left Group
        self.left_group = tk.Frame(self.bot_row, bg="#0D111A")
        self.left_group.pack(side="left")

        # [+] Screen Snapper Button
        self.snap_btn = tk.Button(
            self.left_group,
            text="+",
            bg="#1E293B",
            fg="#94A3B8",
            activebackground="#334155",
            activeforeground="#F1F5F9",
            relief="flat",
            font=("Segoe UI", 12, "bold"),
            width=2,
            bd=0,
            command=self.snap_active_window
        )
        self.snap_btn.pack(side="left", padx=(0, 6))

        # [🌿 Normal ▾] Button
        self.normal_btn = tk.Button(
            self.left_group,
            text="🌿 Normal ▾",
            bg="#1E293B",
            fg="#F8FAFC",
            activebackground="#334155",
            activeforeground="#FFFFFF",
            relief="flat",
            font=("Segoe UI", 9, "bold"),
            bd=0,
            padx=8,
            pady=3,
            command=lambda: self.set_mode("Normal")
        )
        self.normal_btn.pack(side="left", padx=(0, 5))

        # [💡 DeepThink ▾] Button
        self.deepthink_btn = tk.Button(
            self.left_group,
            text="💡 DeepThink ▾",
            bg="#0D111A",
            fg="#94A3B8",
            activebackground="#1E293B",
            activeforeground="#F1F5F9",
            relief="flat",
            font=("Segoe UI", 9, "bold"),
            bd=0,
            padx=8,
            pady=3,
            command=lambda: self.set_mode("DeepThink")
        )
        self.deepthink_btn.pack(side="left", padx=(0, 5))

        # Right Group
        self.right_group = tk.Frame(self.bot_row, bg="#0D111A")
        self.right_group.pack(side="right")

        # Status / Spoken text preview label
        self.status_lbl = tk.Label(
            self.right_group,
            text="",
            bg="#0D111A",
            fg="#38BDF8",
            font=("Segoe UI", 9)
        )
        self.status_lbl.pack(side="left", padx=(0, 8))

        # [🎙️ Voice] Button
        self.voice_btn = tk.Button(
            self.right_group,
            text="🎙️ Voice",
            bg="#1E293B",
            fg="#E2E8F0",
            activebackground="#334155",
            activeforeground="#FFFFFF",
            relief="flat",
            font=("Segoe UI", 9),
            bd=0,
            padx=8,
            pady=3,
            command=self.toggle_voice
        )
        self.voice_btn.pack(side="left", padx=(0, 6))

        # [➤] Submit Gradient Button
        self.submit_btn = tk.Button(
            self.right_group,
            text="➤",
            bg="#8B5CF6",
            fg="#FFFFFF",
            activebackground="#A855F7",
            activeforeground="#FFFFFF",
            relief="flat",
            font=("Segoe UI", 10, "bold"),
            width=3,
            bd=0,
            command=self.on_submit
        )
        self.submit_btn.pack(side="left")

        # ---------------- SLIDE-OUT DIFF DRAWER (Initially Hidden) ----------------
        self.drawer_frame = tk.Frame(
            self.main_pill,
            bg="#0A0E17",
            bd=0,
            highlightthickness=1,
            highlightbackground="#334155"
        )

        # Drawer Header
        self.drawer_header = tk.Frame(self.drawer_frame, bg="#0A0E17")
        self.drawer_header.pack(fill="x", padx=12, pady=(8, 4))

        self.drawer_title = tk.Label(
            self.drawer_header,
            text="Surgical Patch Preview",
            bg="#0A0E17",
            fg="#F8FAFC",
            font=("Segoe UI", 11, "bold")
        )
        self.drawer_title.pack(side="left")

        self.drawer_badge = tk.Label(
            self.drawer_header,
            text="Confidence: 98%",
            bg="#0A0E17",
            fg="#10B981",
            font=("Segoe UI", 10, "bold")
        )
        self.drawer_badge.pack(side="left", padx=8)

        # Drawer Spoken Brief
        self.drawer_summary = tk.Label(
            self.drawer_frame,
            text="",
            bg="#0A0E17",
            fg="#94A3B8",
            wraplength=620,
            justify="left",
            font=("Segoe UI", 9)
        )
        self.drawer_summary.pack(fill="x", padx=12, pady=(0, 6))

        # Unified Diff TextBox
        self.diff_text = tk.Text(
            self.drawer_frame,
            bg="#030712",
            fg="#E2E8F0",
            insertbackground="#38BDF8",
            font=("Consolas", 10),
            height=9,
            relief="flat",
            bd=0
        )
        self.diff_text.tag_configure("add", foreground="#10B981")
        self.diff_text.tag_configure("rem", foreground="#EF4444")
        self.diff_text.pack(fill="both", expand=True, padx=12, pady=(0, 8))

        # Drawer Action Buttons
        self.drawer_actions = tk.Frame(self.drawer_frame, bg="#0A0E17")
        self.drawer_actions.pack(fill="x", padx=12, pady=(0, 8))

        self.apply_btn = tk.Button(
            self.drawer_actions,
            text="▶ Apply Patch & Run Verification Proof",
            bg="#10B981",
            fg="#FFFFFF",
            activebackground="#059669",
            activeforeground="#FFFFFF",
            relief="flat",
            font=("Segoe UI", 10, "bold"),
            bd=0,
            padx=10,
            pady=4,
            command=self.on_apply_patch
        )
        self.apply_btn.pack(side="left", padx=(0, 8))

        self.dismiss_btn = tk.Button(
            self.drawer_actions,
            text="✕ Dismiss",
            bg="#334155",
            fg="#E2E8F0",
            activebackground="#475569",
            activeforeground="#FFFFFF",
            relief="flat",
            font=("Segoe UI", 10),
            bd=0,
            padx=10,
            pady=4,
            command=self.close_drawer
        )
        self.dismiss_btn.pack(side="left")

    def _on_entry_focus_in(self, event):
        if self.input_entry.get() == self.placeholder_text:
            self.input_entry.delete(0, "end")
            self.input_entry.configure(fg="#F1F5F9")

    def _on_entry_focus_out(self, event):
        if not self.input_entry.get().strip():
            self.input_entry.insert(0, self.placeholder_text)
            self.input_entry.configure(fg="#64748B")

    def set_mode(self, mode: str):
        self.active_mode = mode
        if mode == "Normal":
            self.normal_btn.configure(bg="#1E293B", fg="#F8FAFC")
            self.deepthink_btn.configure(bg="#0D111A", fg="#94A3B8")
            self.glow_border.configure(bg="#3B82F6", highlightbackground="#3B82F6")
        else:
            self.deepthink_btn.configure(bg="#1E293B", fg="#F8FAFC")
            self.normal_btn.configure(bg="#0D111A", fg="#94A3B8")
            self.glow_border.configure(bg="#A855F7", highlightbackground="#A855F7")

    def snap_active_window(self):
        """Temporarily hides capsule, captures focused window, and attaches thumbnail."""
        self.withdraw()
        self.after(200, self._do_snap)

    def _do_snap(self):
        saved_path, win_title = WindowSnapper.capture_active_window()
        self.deiconify()
        self.lift()
        self.attributes("-topmost", True)

        if saved_path:
            self.attached_screenshot = saved_path
            self.attached_screenshot_title = win_title
            short_title = (win_title[:14] + "..") if len(win_title) > 16 else win_title
            self.snap_badge.configure(text=f"📷 {short_title} ✕")
            self.snap_badge.pack(side="right", padx=(4, 0))
            self.status_lbl.configure(text=f"Attached: {short_title}")
        else:
            self.status_lbl.configure(text="Snap captured.")

    def clear_attached_screen(self):
        self.attached_screenshot = None
        self.attached_screenshot_title = None
        self.snap_badge.pack_forget()
        self.status_lbl.configure(text="")

    def toggle_voice(self):
        if not self.recording_voice:
            self.recording_voice = True
            self.voice_btn.configure(text="🔴 Stop", bg="#EF4444")
            self.status_lbl.configure(text="Listening...")
            self.voice_recorder.start_recording()
        else:
            self.recording_voice = False
            self.voice_btn.configure(text="🎙️ Voice", bg="#1E293B")
            self.status_lbl.configure(text="Audio captured.")
            self.voice_audio_bytes = self.voice_recorder.stop_recording()
            text_val = self.input_entry.get().strip()
            if not text_val or text_val == self.placeholder_text:
                self.on_submit()

    def on_submit(self):
        prompt = self.input_entry.get().strip()
        if prompt == self.placeholder_text:
            prompt = ""

        if not prompt and not self.attached_screenshot and not self.voice_audio_bytes:
            self.status_lbl.configure(text="Type prompt or snap screen.")
            return

        self.status_lbl.configure(text="Analyzing...")
        self.submit_btn.configure(state="disabled")

        threading.Thread(target=self._run_analysis_worker, args=(prompt,), daemon=True).start()

    def _run_analysis_worker(self, prompt: str):
        try:
            mode_param = "normal" if self.active_mode == "Normal" else "deepthink"
            result = self.bridge.analyze(
                prompt=prompt,
                image_path=self.attached_screenshot,
                audio_bytes=self.voice_audio_bytes,
                mode=mode_param
            )
            self.after(0, lambda: self._handle_analysis_result(result))
        except Exception as e:
            self.after(0, lambda: self._handle_analysis_error(str(e)))

    def _handle_analysis_result(self, result: Dict[str, Any]):
        self.submit_btn.configure(state="normal")
        self.latest_diagnosis = result["diagnosis"]
        action_type = result["action_type"]

        self.status_lbl.configure(text=f"Path: {action_type.upper()}")

        if action_type == "fix" and result.get("diff_preview"):
            self.open_drawer(result)
        else:
            self.input_entry.delete(0, "end")
            self.input_entry.insert(0, result["spoken_summary"])
            self.input_entry.configure(fg="#F1F5F9")
            if self.is_drawer_open:
                self.close_drawer()

    def _handle_analysis_error(self, err_msg: str):
        self.submit_btn.configure(state="normal")
        self.status_lbl.configure(text="Error.")
        self.input_entry.delete(0, "end")
        self.input_entry.insert(0, f"Error: {err_msg[:50]}")
        self.input_entry.configure(fg="#EF4444")

    def open_drawer(self, result: Dict[str, Any]):
        self.is_drawer_open = True
        self.geometry(f"{self.capsule_width}x{self.capsule_height + self.drawer_height}")

        self.drawer_title.configure(text=f"Surgical Fix: {self.latest_diagnosis.evidence.suspect_file or 'Code'}")
        self.drawer_badge.configure(text=f"Confidence: {int(result['confidence'] * 100)}%")
        self.drawer_summary.configure(text=result["spoken_summary"])

        self.diff_text.delete("1.0", "end")
        diff_content = result.get("diff_preview", "")
        for line in diff_content.splitlines(keepends=True):
            if line.startswith("+"):
                self.diff_text.insert("end", line, "add")
            elif line.startswith("-"):
                self.diff_text.insert("end", line, "rem")
            else:
                self.diff_text.insert("end", line)

        self.drawer_frame.pack(fill="both", expand=True, padx=12, pady=(0, 8))

    def close_drawer(self):
        self.is_drawer_open = False
        self.drawer_frame.pack_forget()
        self.geometry(f"{self.capsule_width}x{self.capsule_height}")

    def on_apply_patch(self):
        if not self.latest_diagnosis:
            return

        self.apply_btn.configure(text="Applying & Verifying...", state="disabled")
        threading.Thread(target=self._apply_patch_worker, daemon=True).start()

    def _apply_patch_worker(self):
        try:
            res = self.bridge.apply_patch_and_verify(self.latest_diagnosis)
            self.after(0, lambda: self._handle_patch_result(res))
        except Exception as e:
            self.after(0, lambda: self._handle_patch_error(str(e)))

    def _handle_patch_result(self, res: Dict[str, Any]):
        self.apply_btn.configure(text="✔ Patch Applied & Verified", state="normal", bg="#3B82F6")
        self.status_lbl.configure(text=f"Branch: {res.get('branch', 'Verified')}")
        self.after(2000, self.close_drawer)

    def _handle_patch_error(self, err_msg: str):
        self.apply_btn.configure(text="Verification Failed", state="normal", bg="#EF4444")
        self.status_lbl.configure(text=err_msg[:30])


def launch_capsule():
    app = FloatingCapsule()
    app.mainloop()


if __name__ == "__main__":
    launch_capsule()
