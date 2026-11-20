"""
V.E.R.D.A.N.T. Desktop Floating Capsule - Universal Application Launcher
Launches the hardware-accelerated floating capsule window matching the reference design:
    python capsule/app.py
"""
import sys
import os
from pathlib import Path

# Add project root to sys.path
root_dir = Path(__file__).resolve().parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from capsule.web_capsule import main as launch_app_window


def main():
    print("=" * 65)
    print("🌿 V.E.R.D.A.N.T. v2 Desktop Floating Capsule")
    print("Multimodal Desktop Sentinel for Google Cloud & DeepMind")
    print("=" * 65)

    try:
        launch_app_window()
    except Exception as e:
        print(f"[Capsule] Error launching app window: {e}")
        # Fallback to local browser URL
        import webbrowser
        webbrowser.open("http://127.0.0.1:8000/capsule")


if __name__ == "__main__":
    main()
