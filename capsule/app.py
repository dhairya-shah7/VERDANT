"""
V.E.R.D.A.N.T. v2 — Floating Capsule Launcher
Starts server.py then opens Chrome/Edge in --app mode.
No Tkinter. No CustomTkinter. No GUI frameworks.
"""
import os
import sys
import time
import signal
import socket
import subprocess
import urllib.request
from pathlib import Path

# ─── Paths ───────────────────────────────────────────────────────────────────
ROOT = Path(__file__).resolve().parent.parent
SERVER_SCRIPT = ROOT / "server.py"

CAPSULE_URL = "http://127.0.0.1:8000/capsule"
HEALTH_URL  = "http://127.0.0.1:8000/api/health"

# ─── Browser candidates (Chrome first, Edge fallback, Brave last) ─────────────
BROWSER_CANDIDATES = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
]

# ─── Window geometry (top-center, 1280×800 screen @ 150% DPI) ────────────────
# Physical pixels: 1280×800. At 150% DPI the browser uses logical pixels.
# We want the capsule at the very top-center.
WIN_W  = 700
WIN_H  = 110
WIN_X  = (1280 - WIN_W) // 2   # 290
WIN_Y  = 20                     # 20px from top


def _kill_port(port: int) -> None:
    """Kill any process listening on port."""
    try:
        result = subprocess.run(
            ["netstat", "-ano"],
            capture_output=True, text=True
        )
        for line in result.stdout.splitlines():
            if f":{port}" in line and "LISTENING" in line:
                parts = line.split()
                pid = int(parts[-1])
                subprocess.run(["taskkill", "/PID", str(pid), "/F"],
                               capture_output=True)
                print(f"[Capsule] Killed PID {pid} on port {port}")
    except Exception as e:
        print(f"[Capsule] Port cleanup: {e}")


def _is_port_open(port: int) -> bool:
    """Quick TCP probe."""
    try:
        with socket.create_connection(("127.0.0.1", port), timeout=1):
            return True
    except OSError:
        return False


def _wait_for_server(timeout: int = 20) -> bool:
    """Poll until server is up or timeout."""
    deadline = time.time() + timeout
    while time.time() < deadline:
        if _is_port_open(8000):
            try:
                urllib.request.urlopen(HEALTH_URL, timeout=2)
                return True
            except Exception:
                pass
        time.sleep(0.4)
    return False


def _find_browser() -> str | None:
    for path in BROWSER_CANDIDATES:
        if Path(path).exists():
            return path
    return None


def _launch_app_window(browser_path: str, server_proc: subprocess.Popen) -> None:
    """Open the browser in --app mode as a floating top-of-screen capsule."""
    # Build the user-data-dir so it's isolated from normal browser profile
    user_data = ROOT / ".capsule_profile"
    user_data.mkdir(exist_ok=True)

    cmd = [
        browser_path,
        f"--app={CAPSULE_URL}",
        f"--window-position={WIN_X},{WIN_Y}",
        f"--window-size={WIN_W},{WIN_H}",
        "--no-first-run",
        "--no-default-browser-check",
        "--disable-extensions",
        "--disable-background-networking",
        "--disable-sync",
        "--disable-translate",
        "--disable-features=TranslateUI",
        "--disable-infobars",
        f"--user-data-dir={user_data}",
    ]

    print(f"[Capsule] Launching: {Path(browser_path).name}")
    print(f"[Capsule] Position:  ({WIN_X}, {WIN_Y})  Size: {WIN_W}×{WIN_H}")
    print(f"[Capsule] URL:       {CAPSULE_URL}")

    browser_proc = subprocess.Popen(cmd)

    print("[Capsule] ✅ App window launched — look at the TOP-CENTER of your screen.")
    print("[Capsule] Press Ctrl+C here to stop server + capsule.")

    try:
        # Keep this process alive so server.py stays running
        while True:
            if server_proc.poll() is not None:
                print("[Capsule] ⚠️  Server exited unexpectedly. Restarting…")
                server_proc = subprocess.Popen(
                    [sys.executable, str(SERVER_SCRIPT)],
                    cwd=str(ROOT),
                )
            time.sleep(2)
    except KeyboardInterrupt:
        print("\n[Capsule] Shutting down…")
        browser_proc.terminate()
        server_proc.terminate()
        sys.exit(0)


def main() -> None:
    print("=" * 60)
    print("🌿 V.E.R.D.A.N.T. v2 Floating Capsule")
    print("   Chrome/Edge --app mode, no Tkinter")
    print("=" * 60)

    # 1. Kill anything on port 8000
    _kill_port(8000)
    time.sleep(0.5)

    # 2. Find browser
    browser_path = _find_browser()
    if not browser_path:
        print("[Capsule] ❌ No Chrome/Edge/Brave found. Install Chrome and retry.")
        sys.exit(1)

    # 3. Start server.py
    print(f"[Capsule] Starting server: {SERVER_SCRIPT}")
    env = {**os.environ}
    # Load .env manually
    env_file = ROOT / ".env"
    if env_file.exists():
        for line in env_file.read_text().splitlines():
            line = line.strip()
            if line and "=" in line and not line.startswith("#"):
                k, v = line.split("=", 1)
                env[k.strip()] = v.strip()

    server_proc = subprocess.Popen(
        [sys.executable, str(SERVER_SCRIPT)],
        cwd=str(ROOT),
        env=env,
    )

    # 4. Wait for server to be ready
    print("[Capsule] Waiting for server on :8000 …")
    if not _wait_for_server(timeout=20):
        print("[Capsule] ❌ Server did not start in 20 s. Check server.py for errors.")
        server_proc.terminate()
        sys.exit(1)
    print("[Capsule] ✅ Server is live!")

    # 5. Launch browser --app window
    _launch_app_window(browser_path, server_proc)


if __name__ == "__main__":
    main()
