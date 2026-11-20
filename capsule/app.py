"""
V.E.R.D.A.N.T. Desktop Floating Capsule - Application Entrypoint
Run this script to launch the native desktop floating capsule:
    python capsule/app.py
"""
import sys
from pathlib import Path

# Add project root to sys.path
root_dir = Path(__file__).resolve().parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from capsule.ui import FloatingCapsule
from capsule.hotkey import register_global_hotkey


def main():
    print("=" * 65)
    print("🌿 V.E.R.D.A.N.T. v2 Desktop Floating Capsule")
    print("Always-on-top, draggable desktop sentinel for Google Cloud & DeepMind")
    print("=" * 65)

    app = FloatingCapsule()

    # Safely schedule UI visibility toggle onto the main Tkinter thread
    def on_hotkey_pressed():
        try:
            app.after(0, app.toggle_visibility)
        except Exception:
            pass

    try:
        register_global_hotkey("ctrl+shift+space", on_hotkey_pressed)
        register_global_hotkey("alt+space", on_hotkey_pressed)
    except Exception as e:
        print(f"[Capsule] Hotkey listener notice: {e}")

    print("[Capsule] Native floating capsule window is now active.")
    print("[Capsule] Window Title: '🌿 V.E.R.D.A.N.T. Capsule' (Anchored in Taskbar & Always-on-Top).")
    
    app.mainloop()


if __name__ == "__main__":
    main()
