"""
V.E.R.D.A.N.T. Desktop Capsule - Global Hotkey Listener
Hooks [Ctrl + Shift + Space] or [Alt + Space] to toggle capsule visibility across Windows.
"""
from typing import Callable
import threading

try:
    import keyboard
    HAS_KEYBOARD = True
except ImportError:
    HAS_KEYBOARD = False


def register_global_hotkey(hotkey: str, callback: Callable):
    """
    Registers a background global hotkey listener on Windows.
    Default hotkey: 'ctrl+shift+space' or 'alt+space'.
    """
    if not HAS_KEYBOARD:
        print("[Hotkey] 'keyboard' module not installed; hotkey disabled.")
        return

    def _listen():
        try:
            keyboard.add_hotkey(hotkey, callback)
            keyboard.wait()
        except Exception as e:
            print(f"[Hotkey] Error registering {hotkey}: {e}")

    listener_thread = threading.Thread(target=_listen, daemon=True)
    listener_thread.start()
