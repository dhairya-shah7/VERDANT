"""
V.E.R.D.A.N.T. Desktop Floating Capsule UI
Always-on-top, responsive desktop sentinel:
- Sleek dark aesthetic (#0D111A) with neon accent border (#3B82F6 / #A855F7)
- Guaranteed Taskbar presence & stay-on-top floating behavior
- Text input with '| Ask anything...' placeholder
- Controls: [+] attach screen, [🌿 Normal / 💡 DeepThink] mode toggles, [🎙️ Voice] push-to-talk, [➤] submit
- Toggleable Frameless / Titlebar mode
- Expandable slide-out diff drawer for surgical patches with 1-click apply and proof verification
"""
import threading
from pathlib import Path
from typing import Optional, Dict, Any
import tkinter as tk
import customtkinter as ctk

from .snapper import WindowSnapper
from .voice import VoiceRecorder
from .bridge import CapsuleBridge

# CustomTkinter Theme Settings
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class FloatingCapsule(ctk.CTk):
    def __init__(self, frameless: bool = False):
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
        self.is_frameless = frameless

        # Window Title & Attributes (Guaranteed Taskbar Presence)
        self.title("🌿 V.E.R.D.A.N.T. Floating Capsule")
        self.attributes("-topmost", True)
        if self.is_frameless:
            self.overrideredirect(True)

        # Initial Dimensions & Center on Top of Screen
        screen_w = self.winfo_screenwidth()
        self.capsule_width = 720
        self.capsule_height = 115
        self.drawer_height = 360
        init_x = max(30, int((screen_w - self.capsule_width) / 2))
        init_y = 60
        self.geometry(f"{self.capsule_width}x{self.capsule_height}+{init_x}+{init_y}")

        # Drag Window Handlers
        self._drag_data = {"x": 0, "y": 0}

        self._build_ui()
        self._bind_drag(self.glow_border)
        self._bind_drag(self.main_pill)

        # Ensure Immediate Visibility
        self.deiconify()
        self.lift()
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

    def toggle_frameless(self):
        """Toggles between standard titlebar and frameless pill."""
        self.is_frameless = not self.is_frameless
        self.overrideredirect(self.is_frameless)
        self.deiconify()
        self.lift()

    def toggle_visibility(self):
        """Toggles show/hide safely on main thread."""
        if self.is_visible:
            self.withdraw()
            self.is_visible = False
        else:
            self.deiconify()
            self.lift()
            self.focus_force()
            self.is_visible = True

    def _build_ui(self):
        # Outer Glowing Frame (Simulates Neon Ambient Rim)
        self.glow_border = ctk.CTkFrame(
            self,
            fg_color="#090D16",
            corner_radius=20,
            border_width=2,
            border_color="#3B82F6"
        )
        self.glow_border.pack(fill="both", expand=True, padx=4, pady=4)

        # Main Capsule Pill Body
        self.main_pill = ctk.CTkFrame(
            self.glow_border,
            fg_color="#0D111A",
            corner_radius=18,
            border_width=0
        )
        self.main_pill.pack(fill="both", expand=True, padx=2, pady=2)

        # ---------------- TOP ROW: Prompt Input & Snapped Badge ----------------
        self.top_row = ctk.CTkFrame(self.main_pill, fg_color="transparent")
        self.top_row.pack(fill="x", padx=14, pady=(10, 4))

        self.input_entry = ctk.CTkEntry(
            self.top_row,
            placeholder_text="| Ask anything... (e.g. 'Fix the cart bug' or 'Explain error')",
            placeholder_text_color="#64748B",
            fg_color="transparent",
            text_color="#F1F5F9",
            font=ctk.CTkFont(family="Segoe UI", size=14),
            border_width=0,
            height=34
        )
        self.input_entry.pack(side="left", fill="x", expand=True)
        self.input_entry.bind("<Return>", lambda e: self.on_submit())

        # Screenshot Thumbnail / Badge (Initially Hidden)
        self.snap_badge = ctk.CTkButton(
            self.top_row,
            text="",
            fg_color="#1E293B",
            hover_color="#334155",
            text_color="#38BDF8",
            corner_radius=12,
            height=26,
            font=ctk.CTkFont(size=11, weight="bold"),
            command=self.clear_attached_screen
        )

        # Window Controls: Minimize [-] and Close [x]
        self.win_controls = ctk.CTkFrame(self.top_row, fg_color="transparent")
        self.win_controls.pack(side="right", padx=(6, 0))

        self.min_btn = ctk.CTkButton(
            self.win_controls,
            text="—",
            width=24,
            height=24,
            corner_radius=12,
            fg_color="transparent",
            hover_color="#1E293B",
            text_color="#94A3B8",
            font=ctk.CTkFont(size=12, weight="bold"),
            command=self.toggle_visibility
        )
        self.min_btn.pack(side="left", padx=2)

        self.close_btn = ctk.CTkButton(
            self.win_controls,
            text="✕",
            width=24,
            height=24,
            corner_radius=12,
            fg_color="transparent",
            hover_color="#EF4444",
            text_color="#94A3B8",
            font=ctk.CTkFont(size=12, weight="bold"),
            command=self.destroy
        )
        self.close_btn.pack(side="left", padx=2)

        # ---------------- BOTTOM ROW: Mode, Attachment, Voice, Submit ----------------
        self.bot_row = ctk.CTkFrame(self.main_pill, fg_color="transparent")
        self.bot_row.pack(fill="x", padx=14, pady=(4, 10))

        # Left Group
        self.left_group = ctk.CTkFrame(self.bot_row, fg_color="transparent")
        self.left_group.pack(side="left")

        # [+] Screen Snapper Button
        self.snap_btn = ctk.CTkButton(
            self.left_group,
            text="+",
            width=30,
            height=30,
            corner_radius=15,
            fg_color="#1E293B",
            hover_color="#334155",
            text_color="#94A3B8",
            font=ctk.CTkFont(size=17, weight="bold"),
            command=self.snap_active_window
        )
        self.snap_btn.pack(side="left", padx=(0, 8))

        # [🌿 Normal] Button
        self.normal_btn = ctk.CTkButton(
            self.left_group,
            text="🌿 Normal",
            width=85,
            height=28,
            corner_radius=14,
            fg_color="#1E293B",
            hover_color="#334155",
            text_color="#F8FAFC",
            font=ctk.CTkFont(size=11, weight="bold"),
            command=lambda: self.set_mode("Normal")
        )
        self.normal_btn.pack(side="left", padx=(0, 6))

        # [💡 DeepThink] Button
        self.deepthink_btn = ctk.CTkButton(
            self.left_group,
            text="💡 DeepThink",
            width=100,
            height=28,
            corner_radius=14,
            fg_color="transparent",
            hover_color="#1E293B",
            text_color="#94A3B8",
            font=ctk.CTkFont(size=11, weight="bold"),
            command=lambda: self.set_mode("DeepThink")
        )
        self.deepthink_btn.pack(side="left", padx=(0, 6))

        # Right Group
        self.right_group = ctk.CTkFrame(self.bot_row, fg_color="transparent")
        self.right_group.pack(side="right")

        # Status / Spoken text preview label
        self.status_lbl = ctk.CTkLabel(
            self.right_group,
            text="",
            text_color="#38BDF8",
            font=ctk.CTkFont(size=11)
        )
        self.status_lbl.pack(side="left", padx=(0, 10))

        # [🎙️ Voice] Button
        self.voice_btn = ctk.CTkButton(
            self.right_group,
            text="🎙️ Voice",
            width=75,
            height=28,
            corner_radius=14,
            fg_color="#1E293B",
            hover_color="#334155",
            text_color="#E2E8F0",
            font=ctk.CTkFont(size=11),
            command=self.toggle_voice
        )
        self.voice_btn.pack(side="left", padx=(0, 8))

        # [➤] Submit Gradient Button
        self.submit_btn = ctk.CTkButton(
            self.right_group,
            text="➤",
            width=32,
            height=32,
            corner_radius=16,
            fg_color="#8B5CF6",
            hover_color="#A855F7",
            text_color="#FFFFFF",
            font=ctk.CTkFont(size=13, weight="bold"),
            command=self.on_submit
        )
        self.submit_btn.pack(side="left")

        # ---------------- SLIDE-OUT DIFF DRAWER (Initially Hidden) ----------------
        self.drawer_frame = ctk.CTkFrame(
            self.main_pill,
            fg_color="#0A0E17",
            corner_radius=14,
            border_width=1,
            border_color="#334155"
        )

        # Drawer Header
        self.drawer_header = ctk.CTkFrame(self.drawer_frame, fg_color="transparent")
        self.drawer_header.pack(fill="x", padx=14, pady=(10, 4))

        self.drawer_title = ctk.CTkLabel(
            self.drawer_header,
            text="Surgical Patch Preview",
            text_color="#F8FAFC",
            font=ctk.CTkFont(size=13, weight="bold")
        )
        self.drawer_title.pack(side="left")

        self.drawer_badge = ctk.CTkLabel(
            self.drawer_header,
            text="Confidence: 98%",
            text_color="#10B981",
            font=ctk.CTkFont(size=11, weight="bold")
        )
        self.drawer_badge.pack(side="left", padx=10)

        # Drawer Spoken Brief
        self.drawer_summary = ctk.CTkLabel(
            self.drawer_frame,
            text="",
            text_color="#94A3B8",
            wraplength=660,
            justify="left",
            font=ctk.CTkFont(size=11)
        )
        self.drawer_summary.pack(fill="x", padx=14, pady=(0, 6))

        # Unified Diff TextBox
        self.diff_text = ctk.CTkTextbox(
            self.drawer_frame,
            fg_color="#030712",
            text_color="#E2E8F0",
            font=ctk.CTkFont(family="Consolas", size=11),
            height=160,
            corner_radius=8
        )
        self.diff_text.pack(fill="both", expand=True, padx=14, pady=(0, 8))

        # Drawer Action Buttons
        self.drawer_actions = ctk.CTkFrame(self.drawer_frame, fg_color="transparent")
        self.drawer_actions.pack(fill="x", padx=14, pady=(0, 10))

        self.apply_btn = ctk.CTkButton(
            self.drawer_actions,
            text="▶ Apply Patch & Run Verification Proof",
            fg_color="#10B981",
            hover_color="#059669",
            text_color="#FFFFFF",
            font=ctk.CTkFont(size=11, weight="bold"),
            height=30,
            command=self.on_apply_patch
        )
        self.apply_btn.pack(side="left", padx=(0, 8))

        self.dismiss_btn = ctk.CTkButton(
            self.drawer_actions,
            text="✕ Dismiss",
            fg_color="#334155",
            hover_color="#475569",
            text_color="#E2E8F0",
            font=ctk.CTkFont(size=11),
            height=30,
            command=self.close_drawer
        )
        self.dismiss_btn.pack(side="left")

    def set_mode(self, mode: str):
        self.active_mode = mode
        if mode == "Normal":
            self.normal_btn.configure(fg_color="#1E293B", text_color="#F8FAFC")
            self.deepthink_btn.configure(fg_color="transparent", text_color="#94A3B8")
            self.glow_border.configure(border_color="#3B82F6")
        else:
            self.deepthink_btn.configure(fg_color="#1E293B", text_color="#F8FAFC")
            self.normal_btn.configure(fg_color="transparent", text_color="#94A3B8")
            self.glow_border.configure(border_color="#A855F7")

    def snap_active_window(self):
        """Temporarily hides capsule, captures focused window, and attaches thumbnail."""
        self.withdraw()
        self.after(200, self._do_snap)

    def _do_snap(self):
        saved_path, win_title = WindowSnapper.capture_active_window()
        self.deiconify()
        self.lift()

        if saved_path:
            self.attached_screenshot = saved_path
            self.attached_screenshot_title = win_title
            short_title = (win_title[:16] + "..") if len(win_title) > 18 else win_title
            self.snap_badge.configure(text=f"📷 {short_title} ✕")
            self.snap_badge.pack(side="right", padx=(6, 0))
            self.status_lbl.configure(text=f"Attached: {short_title}")
        else:
            self.status_lbl.configure(text="Snap failed.")

    def clear_attached_screen(self):
        self.attached_screenshot = None
        self.attached_screenshot_title = None
        self.snap_badge.pack_forget()
        self.status_lbl.configure(text="")

    def toggle_voice(self):
        if not self.recording_voice:
            self.recording_voice = True
            self.voice_btn.configure(text="🔴 Stop", fg_color="#EF4444")
            self.status_lbl.configure(text="Listening...")
            self.voice_recorder.start_recording()
        else:
            self.recording_voice = False
            self.voice_btn.configure(text="🎙️ Voice", fg_color="#1E293B")
            self.status_lbl.configure(text="Audio captured.")
            self.voice_audio_bytes = self.voice_recorder.stop_recording()
            if not self.input_entry.get().strip():
                self.on_submit()

    def on_submit(self):
        prompt = self.input_entry.get().strip()
        if not prompt and not self.attached_screenshot and not self.voice_audio_bytes:
            self.status_lbl.configure(text="Enter prompt or snap screen.")
            return

        self.status_lbl.configure(text="Analyzing with Gemini...")
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
            if self.is_drawer_open:
                self.close_drawer()

    def _handle_analysis_error(self, err_msg: str):
        self.submit_btn.configure(state="normal")
        self.status_lbl.configure(text="Error analyzing.")
        self.input_entry.delete(0, "end")
        self.input_entry.insert(0, f"Error: {err_msg[:60]}")

    def open_drawer(self, result: Dict[str, Any]):
        self.is_drawer_open = True
        self.geometry(f"{self.capsule_width}x{self.capsule_height + self.drawer_height}")

        self.drawer_title.configure(text=f"Surgical Fix: {self.latest_diagnosis.evidence.suspect_file or 'Code'}")
        self.drawer_badge.configure(text=f"Confidence: {int(result['confidence'] * 100)}%")
        self.drawer_summary.configure(text=result["spoken_summary"])

        self.diff_text.delete("1.0", "end")
        self.diff_text.insert("1.0", result["diff_preview"])

        self.drawer_frame.pack(fill="both", expand=True, padx=14, pady=(0, 10))

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
        self.apply_btn.configure(text="✔ Patch Applied & Verified", state="normal", fg_color="#3B82F6")
        self.status_lbl.configure(text=f"Branch: {res.get('branch', 'Verified')}")
        self.after(2000, self.close_drawer)

    def _handle_patch_error(self, err_msg: str):
        self.apply_btn.configure(text="Verification Failed", state="normal", fg_color="#EF4444")
        self.status_lbl.configure(text=err_msg[:40])


def launch_capsule():
    app = FloatingCapsule()
    app.mainloop()


if __name__ == "__main__":
    launch_capsule()
