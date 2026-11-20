"""
V.E.R.D.A.N.T. Desktop Floating Capsule - Active Window Snapper
Uses Windows win32gui and PIL to capture strictly the foreground window
(VS Code, Chrome, Terminal, Postman, etc.) without clutter or background noise.
"""
from typing import Optional, Tuple
from pathlib import Path
import time
from PIL import Image, ImageGrab

try:
    import win32gui
    import win32process
    HAS_WIN32 = True
except ImportError:
    HAS_WIN32 = False


class WindowSnapper:
    """Captures active foreground window or full desktop screen on demand."""

    @staticmethod
    def get_foreground_window_title() -> str:
        """Returns the title of the active foreground window."""
        if not HAS_WIN32:
            return "Active Desktop"
        try:
            hwnd = win32gui.GetForegroundWindow()
            title = win32gui.GetWindowText(hwnd)
            return title if title else "Active Window"
        except Exception:
            return "Active Window"

    @staticmethod
    def capture_active_window(output_path: Optional[Path] = None) -> Tuple[Optional[Path], str]:
        """
        Captures the exact rectangle of the currently focused application window.
        Returns (saved_path, window_title).
        """
        window_title = WindowSnapper.get_foreground_window_title()

        if HAS_WIN32:
            try:
                hwnd = win32gui.GetForegroundWindow()
                rect = win32gui.GetWindowRect(hwnd)
                # rect is (left, top, right, bottom)
                left, top, right, bottom = rect
                width = right - left
                height = bottom - top

                # Only crop if valid window dimensions
                if width > 50 and height > 50:
                    screenshot = ImageGrab.grab(bbox=(left, top, right, bottom), all_screens=True)
                else:
                    screenshot = ImageGrab.grab(all_screens=True)
            except Exception as e:
                print(f"[Snapper] Fallback to full screen: {e}")
                screenshot = ImageGrab.grab(all_screens=True)
        else:
            screenshot = ImageGrab.grab(all_screens=True)

        # Save screenshot
        if not output_path:
            screenshots_dir = Path.cwd() / "uploads" / "captures"
            screenshots_dir.mkdir(parents=True, exist_ok=True)
            timestamp = int(time.time() * 1000)
            output_path = screenshots_dir / f"screen_{timestamp}.png"

        screenshot.save(output_path, "PNG")
        return output_path, window_title

    @staticmethod
    def capture_full_screen(output_path: Optional[Path] = None) -> Path:
        """Captures the entire desktop display across all monitors."""
        screenshot = ImageGrab.grab(all_screens=True)
        if not output_path:
            screenshots_dir = Path.cwd() / "uploads" / "captures"
            screenshots_dir.mkdir(parents=True, exist_ok=True)
            timestamp = int(time.time() * 1000)
            output_path = screenshots_dir / f"fullscreen_{timestamp}.png"

        screenshot.save(output_path, "PNG")
        return output_path
