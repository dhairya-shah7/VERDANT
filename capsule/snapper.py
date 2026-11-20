"""
V.E.R.D.A.N.T. Desktop Floating Capsule - Active Window Snapper
Uses Windows win32gui, mss, and PIL to capture strictly the foreground window
(VS Code, Chrome, Terminal, Postman, etc.) without crashing.
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

try:
    import mss
    HAS_MSS = True
except ImportError:
    HAS_MSS = False


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
    def _grab_with_mss(bbox: Optional[Tuple[int, int, int, int]] = None) -> Optional[Image.Image]:
        """Fallback capture via mss."""
        if not HAS_MSS:
            return None
        try:
            with mss.mss() as sct:
                if bbox:
                    left, top, right, bottom = bbox
                    mon = {"left": left, "top": top, "width": right - left, "height": bottom - top}
                else:
                    mon = sct.monitors[0]
                shot = sct.grab(mon)
                return Image.frombytes("RGB", shot.size, shot.bgra, "raw", "BGRX")
        except Exception as e:
            print(f"[Snapper] mss capture fallback error: {e}")
            return None

    @staticmethod
    def capture_active_window(output_path: Optional[Path] = None) -> Tuple[Optional[Path], str]:
        """
        Captures the exact rectangle of the currently focused application window.
        Returns (saved_path, window_title).
        """
        window_title = WindowSnapper.get_foreground_window_title()
        screenshot: Optional[Image.Image] = None

        if HAS_WIN32:
            try:
                hwnd = win32gui.GetForegroundWindow()
                rect = win32gui.GetWindowRect(hwnd)
                left, top, right, bottom = rect
                width = right - left
                height = bottom - top

                if width > 50 and height > 50:
                    try:
                        screenshot = ImageGrab.grab(bbox=(left, top, right, bottom))
                    except Exception:
                        screenshot = WindowSnapper._grab_with_mss((left, top, right, bottom))
            except Exception as e:
                print(f"[Snapper] Active window rect error: {e}")

        # Fallback to full screen if active window capture did not succeed
        if screenshot is None:
            try:
                screenshot = ImageGrab.grab()
            except Exception:
                screenshot = WindowSnapper._grab_with_mss()

        if screenshot is None:
            return None, window_title

        # Save screenshot
        if not output_path:
            screenshots_dir = Path.cwd() / "uploads" / "captures"
            screenshots_dir.mkdir(parents=True, exist_ok=True)
            timestamp = int(time.time() * 1000)
            output_path = screenshots_dir / f"screen_{timestamp}.png"

        screenshot.save(output_path, "PNG")
        return output_path, window_title
