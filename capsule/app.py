"""
V.E.R.D.A.N.T. Desktop Floating Capsule - Application Entrypoint
Run this script to launch the native desktop floating capsule:
    python -m capsule.app
Or directly:
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
    print("=" * 60)
    print("🌿 V.E.R.D.A.N.T. v2 Desktop Floating Capsule")
    print("Always-on-top, draggable desktop sentinel for Google Cloud & DeepMind")
    print("=" * 60)

    app = FloatingCapsule()

    # Toggle visibility on global hotkey
    def toggle_capsule():
        if app.state() == "normal":
            app.withdraw()
        else:
            app.deiconify()
            app.lift()

    register_global_hotkey("ctrl+shift+space", toggle_capsule)

    print("[Capsule] Running. Use Ctrl+Shift+Space to toggle visibility.")
    app.mainloop()


if __name__ == "__main__":
    main()
