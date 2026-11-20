"""
V.E.R.D.A.N.T. v2 — Native Windows Desktop Floating Capsule Launcher
Hardware-accelerated WPF floating pill anchored always-on-top.
Zero browser dependencies. Fully wired to Gemini 3.5 live multimodal reasoning.

Usage:
    python capsule/app.py
"""
import os
import sys
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CAPSULE_DIR = ROOT / "capsule"
EXE_PATH = CAPSULE_DIR / "capsule.exe"
CS_SOURCE = CAPSULE_DIR / "CapsuleWindow.cs"

CSC_PATH = Path(r"C:\Windows\Microsoft.NET\Framework64\v4.0.30319\csc.exe")

def ensure_compiled():
    # If capsule.exe missing or older than CapsuleWindow.cs, recompile
    if not EXE_PATH.exists() or (CS_SOURCE.exists() and CS_SOURCE.stat().st_mtime > EXE_PATH.stat().st_mtime):
        print("⚙️  Compiling native Windows WPF Capsule binary...")
        cmd = [
            str(CSC_PATH),
            "/target:winexe",
            f"/out:{EXE_PATH}",
            r"/r:C:\Windows\Microsoft.NET\Framework64\v4.0.30319\WPF\PresentationFramework.dll",
            r"/r:C:\Windows\Microsoft.NET\Framework64\v4.0.30319\WPF\PresentationCore.dll",
            r"/r:C:\Windows\Microsoft.NET\Framework64\v4.0.30319\WPF\WindowsBase.dll",
            r"/r:System.dll",
            r"/r:System.Xaml.dll",
            r"/r:System.Core.dll",
            r"/r:C:\Windows\Microsoft.NET\Framework64\v4.0.30319\System.Web.Extensions.dll",
            str(CS_SOURCE),
        ]
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode != 0:
            print(f"❌ Compilation failed:\n{res.stderr or res.stdout}")
            sys.exit(1)
        print("✅ Native Capsule binary ready.")

def main():
    ensure_compiled()
    print("=" * 60)
    print("🌿 V.E.R.D.A.N.T. Native Windows Desktop Capsule Active")
    print("   WPF Hardware-Accelerated Floating Pill")
    print("   Anchored Always-On-Top · Centered at Top of Display")
    print("   Live Gemini 3.5 Multimodal Engine Connected")
    print("   Press Ctrl+C in this terminal or click ✕ on pill to exit")
    print("=" * 60)

    try:
        proc = subprocess.Popen([str(EXE_PATH)], cwd=str(ROOT))
        proc.wait()
    except KeyboardInterrupt:
        if proc.poll() is None:
            proc.terminate()
        print("\n🌿 Capsule closed.")

if __name__ == "__main__":
    main()
