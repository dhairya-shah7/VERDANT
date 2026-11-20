"""
V.E.R.D.A.N.T. v2 — Native Desktop Floating AI Capsule
Pure desktop floating window using pywebview & WebView2.
Runs standalone with zero browser windows, zero servers, always on top.

Usage:
    python capsule/app.py
"""
import os
import sys
import json
import threading
from pathlib import Path

# Setup paths and environment
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

# Load .env variables
env_file = ROOT / ".env"
if env_file.exists():
    for line in env_file.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and "=" in line and not line.startswith("#"):
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip())

import webview
from capsule.bridge import CapsuleBridge
from capsule.snapper import WindowSnapper

# ── Dimensions ───────────────────────────────────────────────────────────────
WIN_W = 640
COLLAPSED_H = 68
EXPANDED_H = 390
WIN_X = (1280 - WIN_W) // 2  # 320 on 1280x800
WIN_Y = 20


# Global reference to avoid .NET SyncRoot recursion during pywebview introspection
_window_ref = [None]


class CapsuleJSAPI:
    """Methods callable from the floating pill HTML via window.pywebview.api.*"""

    def __init__(self):
        self.bridge = CapsuleBridge(ROOT)
        self.last_diagnosis = None
        self.snapped_image_path = None

    def expand(self, height=EXPANDED_H):
        win = _window_ref[0]
        if win:
            win.resize(WIN_W, int(height))
        return True

    def collapse(self):
        win = _window_ref[0]
        if win:
            win.resize(WIN_W, COLLAPSED_H)
        return True

    def minimize(self):
        win = _window_ref[0]
        if win:
            win.minimize()
        return True

    def close(self):
        def _exit():
            import time
            time.sleep(0.1)
            win = _window_ref[0]
            if win:
                win.destroy()
            sys.exit(0)
        threading.Thread(target=_exit, daemon=True).start()
        return True

    def snap_window(self):
        """Captures the active window under the capsule."""
        try:
            path, title = WindowSnapper.capture_active_window()
            if path and path.exists():
                self.snapped_image_path = path
                return {
                    "success": True,
                    "title": title,
                    "path": str(path)
                }
            return {"success": False, "error": "Screen capture returned no image"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def ask(self, prompt: str, mode: str = "normal"):
        """Sends prompt + optional snapped screenshot directly to live Gemini Multimodal."""
        try:
            res = self.bridge.analyze(
                prompt=prompt,
                image_path=self.snapped_image_path,
                mode="deepthink" if mode == "deep" else "normal"
            )
            self.last_diagnosis = res.get("diagnosis")
            
            # Serialize for JS
            diff_text = res.get("diff_preview", "")
            action_type = res.get("action_type", "advise")
            confidence = res.get("confidence", 0.95)
            summary = res.get("spoken_summary", "")
            root_cause = res.get("root_cause", "")
            eco = res.get("eco_audit", {})
            eco_co2 = eco.get("co2_grams", 0.05) if isinstance(eco, dict) else 0.05

            return {
                "success": True,
                "action_type": action_type,
                "confidence": confidence,
                "spoken_summary": summary,
                "root_cause": root_cause,
                "diff": diff_text,
                "eco_co2": f"{eco_co2:.2f}g CO₂",
                "patch_valid": res.get("patch_valid", False)
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    def apply_patch(self):
        """Applies the verified code patch and commits via GitOps."""
        if not self.last_diagnosis:
            return {"success": False, "error": "No active diagnosis to patch"}
        try:
            res = self.bridge.apply_patch_and_verify(self.last_diagnosis)
            return res
        except Exception as e:
            return {"success": False, "error": str(e)}


CAPSULE_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  
  html, body {
    width: 100%;
    height: 100%;
    background: transparent;
    overflow: hidden;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    user-select: none;
    -webkit-user-select: none;
  }

  /* ── Capsule Floating Pill ── */
  #pill {
    width: calc(100% - 16px);
    margin: 6px auto;
    background: rgba(11, 15, 25, 0.98);
    border: 1.5px solid rgba(59, 130, 246, 0.55);
    border-radius: 20px;
    padding: 8px 12px;
    box-shadow:
      0 0 0 1px rgba(0, 0, 0, 0.6),
      0 10px 30px rgba(0, 0, 0, 0.8),
      0 0 25px rgba(59, 130, 246, 0.2);
    display: flex;
    flex-direction: column;
    gap: 7px;
    transition: border-color 0.25s, box-shadow 0.25s;
  }
  #pill.deep {
    border-color: rgba(168, 85, 247, 0.65);
    box-shadow:
      0 0 0 1px rgba(0, 0, 0, 0.6),
      0 10px 30px rgba(0, 0, 0, 0.8),
      0 0 25px rgba(168, 85, 247, 0.25);
  }

  /* ── Drag Region ── */
  .pywebview-drag-region {
    cursor: grab;
  }
  .pywebview-drag-region:active {
    cursor: grabbing;
  }

  /* ── Top Bar / Action Controls ── */
  .bar {
    display: flex;
    align-items: center;
    gap: 8px;
  }

  .brand {
    display: flex;
    align-items: center;
    gap: 5px;
    font-size: 13px;
    font-weight: 800;
    letter-spacing: -0.3px;
    background: linear-gradient(135deg, #60a5fa, #3b82f6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    padding: 0 4px;
    flex-shrink: 0;
  }
  .brand span {
    font-size: 14px;
    -webkit-text-fill-color: initial;
  }

  /* ── Input Box ── */
  #query-input {
    flex: 1;
    min-width: 0;
    background: rgba(255, 255, 255, 0.06);
    border: 1px solid rgba(255, 255, 255, 0.12);
    border-radius: 12px;
    padding: 7px 12px;
    color: #f1f5f9;
    font-size: 12.5px;
    outline: none;
    transition: border-color 0.2s, background 0.2s;
  }
  #query-input::placeholder {
    color: rgba(148, 163, 184, 0.5);
  }
  #query-input:focus {
    border-color: rgba(59, 130, 246, 0.7);
    background: rgba(255, 255, 255, 0.09);
  }

  /* ── Buttons ── */
  .btn {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    border: none;
    outline: none;
    cursor: pointer;
    border-radius: 10px;
    font-weight: 600;
    font-size: 12px;
    transition: all 0.15s ease;
    white-space: nowrap;
    flex-shrink: 0;
  }
  .btn-ask {
    background: linear-gradient(135deg, #3b82f6, #2563eb);
    color: #ffffff;
    padding: 7px 13px;
    box-shadow: 0 2px 8px rgba(37, 99, 235, 0.35);
  }
  .btn-ask:hover {
    filter: brightness(1.15);
    transform: translateY(-1px);
  }
  .btn-ask:active {
    transform: translateY(1px);
  }
  .btn-ask:disabled {
    opacity: 0.6;
    cursor: not-allowed;
    transform: none;
  }

  .btn-snap {
    background: rgba(255, 255, 255, 0.06);
    color: #94a3b8;
    border: 1px solid rgba(255, 255, 255, 0.1);
    padding: 6px 9px;
    font-size: 13px;
  }
  .btn-snap:hover {
    background: rgba(255, 255, 255, 0.12);
    color: #f1f5f9;
  }
  .btn-snap.active {
    border-color: rgba(34, 197, 94, 0.5);
    background: rgba(34, 197, 94, 0.15);
    color: #4ade80;
  }

  .btn-mode {
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.08);
    color: #64748b;
    padding: 6px 9px;
    font-size: 11px;
  }
  .btn-mode.active-fast {
    color: #60a5fa;
    border-color: rgba(59, 130, 246, 0.4);
    background: rgba(59, 130, 246, 0.1);
  }
  .btn-mode.active-deep {
    color: #c084fc;
    border-color: rgba(168, 85, 247, 0.4);
    background: rgba(168, 85, 247, 0.1);
  }

  .btn-tool {
    background: transparent;
    color: #64748b;
    padding: 5px 6px;
    font-size: 13px;
  }
  .btn-tool:hover {
    color: #cbd5e1;
    background: rgba(255, 255, 255, 0.07);
  }
  .btn-close:hover {
    color: #f87171;
    background: rgba(239, 68, 68, 0.15);
  }

  /* ── Status Row ── */
  .status-row {
    display: flex;
    align-items: center;
    gap: 7px;
    font-size: 11px;
    color: #64748b;
    padding: 0 4px;
  }
  .dot {
    width: 7px;
    height: 7px;
    border-radius: 50%;
    background: #22c55e;
    flex-shrink: 0;
    box-shadow: 0 0 8px rgba(34, 197, 94, 0.6);
    animation: pulse 2.5s infinite;
  }
  @keyframes pulse {
    0%, 100% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.4; transform: scale(0.85); }
  }
  .dot.busy {
    background: #f59e0b;
    box-shadow: 0 0 8px rgba(245, 158, 11, 0.6);
    animation: spin 0.8s linear infinite;
  }
  .dot.err {
    background: #ef4444;
    box-shadow: 0 0 8px rgba(239, 68, 68, 0.6);
    animation: none;
  }
  #status-msg {
    flex: 1;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }
  .eco-chip {
    font-size: 10px;
    padding: 2px 7px;
    border-radius: 999px;
    background: rgba(34, 197, 94, 0.12);
    color: #4ade80;
    border: 1px solid rgba(34, 197, 94, 0.25);
  }

  /* ── Response Drawer ── */
  #drawer {
    display: none;
    flex-direction: column;
    gap: 8px;
    padding-top: 4px;
    border-top: 1px solid rgba(255, 255, 255, 0.08);
  }
  #drawer.visible {
    display: flex;
  }

  #summary-box {
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 12px;
    padding: 10px 12px;
    font-size: 12px;
    color: #cbd5e1;
    line-height: 1.6;
    max-height: 130px;
    overflow-y: auto;
    white-space: pre-wrap;
    word-break: break-word;
  }

  #diff-container {
    display: none;
    font-family: 'Cascadia Code', 'Consolas', monospace;
    font-size: 11px;
    line-height: 1.5;
    background: #060913;
    border: 1px solid rgba(255, 255, 255, 0.09);
    border-radius: 10px;
    padding: 8px 10px;
    max-height: 140px;
    overflow-y: auto;
  }
  .diff-add { color: #4ade80; }
  .diff-del { color: #f87171; }
  .diff-hunk { color: #818cf8; font-weight: bold; }

  .drawer-footer {
    display: flex;
    align-items: center;
    justify-content: flex-end;
    gap: 8px;
  }
  .btn-dismiss {
    background: rgba(255, 255, 255, 0.06);
    color: #94a3b8;
    padding: 6px 12px;
    border: 1px solid rgba(255, 255, 255, 0.09);
  }
  .btn-dismiss:hover {
    color: #f1f5f9;
  }
  .btn-apply {
    background: linear-gradient(135deg, #22c55e, #16a34a);
    color: #ffffff;
    padding: 6px 14px;
    box-shadow: 0 2px 8px rgba(34, 197, 94, 0.35);
  }
  .btn-apply:hover {
    filter: brightness(1.1);
  }

  /* ── Spinner ── */
  .spin {
    display: inline-block;
    width: 12px;
    height: 12px;
    border: 2px solid rgba(255, 255, 255, 0.3);
    border-top-color: #ffffff;
    border-radius: 50%;
    animation: rotate 0.6s linear infinite;
  }
  @keyframes rotate {
    to { transform: rotate(360deg); }
  }
</style>
</head>
<body>

<div id="pill">
  <!-- TOP CONTROL BAR -->
  <div class="bar">
    <div class="brand pywebview-drag-region" title="Drag to move capsule">
      <span>🌿</span> VERDANT
    </div>

    <input id="query-input" type="text"
           placeholder="Describe defect, paste stack trace, or ask for fix…"
           autocomplete="off" spellcheck="false" />

    <button class="btn btn-snap" id="btn-snap" onclick="snapActiveWindow()" title="Snap Foreground Window (VS Code / App)">📸</button>

    <button class="btn btn-mode active-fast" id="btn-fast" onclick="setMode('fast')" title="Fast Reasoning (Gemini Flash Lite)">⚡</button>
    <button class="btn btn-mode" id="btn-deep" onclick="setMode('deep')" title="DeepThink Multimodal (Gemini Flash)">🧠</button>

    <button class="btn btn-ask" id="btn-ask" onclick="submitQuery()">▶ Ask</button>

    <button class="btn btn-tool" onclick="pywebview.api.minimize()" title="Minimize">➖</button>
    <button class="btn btn-tool btn-close" onclick="pywebview.api.close()" title="Close Capsule">✕</button>
  </div>

  <!-- STATUS ROW -->
  <div class="status-row pywebview-drag-region">
    <div class="dot" id="dot"></div>
    <span id="status-msg">Ready · Gemini 3.5 live</span>
    <span class="eco-chip" id="eco-chip">🌱 0.05g CO₂</span>
  </div>

  <!-- RESPONSE DRAWER -->
  <div id="drawer">
    <div id="summary-box">Thinking…</div>
    <div id="diff-container"></div>
    <div class="drawer-footer">
      <button class="btn btn-dismiss" onclick="dismissDrawer()">Dismiss</button>
      <button class="btn btn-apply" id="btn-apply-patch" style="display:none;" onclick="applyPatch()">▶ Apply Patch &amp; Verify</button>
    </div>
  </div>
</div>

<script>
  let activeMode = 'fast';
  let snappedState = false;

  window.addEventListener('load', () => {
    document.getElementById('query-input').focus();
  });

  document.getElementById('query-input').addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      submitQuery();
    }
  });

  function setMode(mode) {
    activeMode = mode;
    const pill = document.getElementById('pill');
    const btnFast = document.getElementById('btn-fast');
    const btnDeep = document.getElementById('btn-deep');
    if (mode === 'deep') {
      pill.classList.add('deep');
      btnDeep.className = 'btn btn-mode active-deep';
      btnFast.className = 'btn btn-mode';
    } else {
      pill.classList.remove('deep');
      btnFast.className = 'btn btn-mode active-fast';
      btnDeep.className = 'btn btn-mode';
    }
  }

  function setStatus(msg, state='ok') {
    document.getElementById('status-msg').textContent = msg;
    const dot = document.getElementById('dot');
    dot.className = 'dot' + (state === 'busy' ? ' busy' : state === 'err' ? ' err' : '');
  }

  async function snapActiveWindow() {
    const btn = document.getElementById('btn-snap');
    btn.textContent = '⏳';
    setStatus('Capturing active desktop window…', 'busy');
    try {
      const res = await pywebview.api.snap_window();
      if (res.success) {
        snappedState = true;
        btn.textContent = '✅';
        btn.classList.add('active');
        setStatus(`Captured: ${res.title.substring(0, 35)}`, 'ok');
      } else {
        btn.textContent = '📸';
        setStatus('Snap: ' + res.error, 'err');
      }
    } catch(err) {
      btn.textContent = '📸';
      setStatus('Snap error: ' + err, 'err');
    }
  }

  async function submitQuery() {
    const input = document.getElementById('query-input');
    const prompt = input.value.trim();
    if (!prompt) {
      input.focus();
      return;
    }

    const btnAsk = document.getElementById('btn-ask');
    btnAsk.innerHTML = '<span class="spin"></span>';
    btnAsk.disabled = true;

    // Expand window height
    await pywebview.api.expand(390);

    const drawer = document.getElementById('drawer');
    drawer.classList.add('visible');
    document.getElementById('summary-box').textContent = 'Analyzing defect via Google Gemini Multimodal…';
    document.getElementById('diff-container').style.display = 'none';
    document.getElementById('btn-apply-patch').style.display = 'none';

    setStatus('Multimodal reasoning in progress…', 'busy');

    try {
      const res = await pywebview.api.ask(prompt, activeMode);
      if (res.success) {
        let text = `[${res.action_type.toUpperCase()}] Confidence: ${(res.confidence * 100).toFixed(0)}%\n\n`;
        if (res.spoken_summary) text += `${res.spoken_summary}\n\n`;
        if (res.root_cause) text += `Root Cause:\n${res.root_cause}`;

        document.getElementById('summary-box').textContent = text.trim();
        document.getElementById('eco-chip').textContent = `🌱 ${res.eco_co2}`;

        // Render Diff if FIX action
        if (res.diff) {
          renderDiff(res.diff);
          document.getElementById('btn-apply-patch').style.display = 'inline-flex';
        }

        setStatus(`Diagnosis complete · [${res.action_type}]`, 'ok');
      } else {
        document.getElementById('summary-box').textContent = '❌ ' + (res.error || 'Failed to analyze');
        setStatus('Analysis failed', 'err');
      }
    } catch(err) {
      document.getElementById('summary-box').textContent = '❌ ' + err;
      setStatus('Engine error', 'err');
    }

    btnAsk.innerHTML = '▶ Ask';
    btnAsk.disabled = false;
  }

  function renderDiff(diffText) {
    const container = document.getElementById('diff-container');
    container.innerHTML = '';
    const lines = diffText.split('\\n');
    lines.forEach(line => {
      const div = document.createElement('div');
      if (line.startsWith('+')) {
        div.className = 'diff-add';
      } else if (line.startsWith('-')) {
        div.className = 'diff-del';
      } else if (line.startsWith('@@')) {
        div.className = 'diff-hunk';
      }
      div.textContent = line;
      container.appendChild(div);
    });
    container.style.display = 'block';
  }

  async function applyPatch() {
    const btn = document.getElementById('btn-apply-patch');
    btn.innerHTML = '<span class="spin"></span> Applying…';
    btn.disabled = true;
    setStatus('Applying atomic patch & running GitOps verification…', 'busy');

    try {
      const res = await pywebview.api.apply_patch();
      if (res.success) {
        setStatus(`Patch applied & committed! [${res.branch || 'main'}]`, 'ok');
        btn.textContent = '✅ Applied';
      } else {
        setStatus('Patch error: ' + (res.error || 'Unknown'), 'err');
        btn.textContent = 'Retry Patch';
        btn.disabled = false;
      }
    } catch(err) {
      setStatus('Apply error: ' + err, 'err');
      btn.textContent = 'Retry Patch';
      btn.disabled = false;
    }
  }

  async function dismissDrawer() {
    const drawer = document.getElementById('drawer');
    drawer.classList.remove('visible');
    document.getElementById('diff-container').style.display = 'none';
    document.getElementById('btn-apply-patch').style.display = 'none';
    await pywebview.api.collapse();
    setStatus('Ready · Gemini 3.5 live', 'ok');
  }
</script>
</body>
</html>
"""

def main():
    api = CapsuleJSAPI()

    window = webview.create_window(
        title="🌿 V.E.R.D.A.N.T. Capsule",
        html=CAPSULE_HTML,
        js_api=api,
        width=WIN_W,
        height=COLLAPSED_H,
        x=WIN_X,
        y=WIN_Y,
        frameless=True,
        on_top=True,
        transparent=True,
        easy_drag=True,
        resizable=True,
        min_size=(WIN_W, COLLAPSED_H)
    )
    _window_ref[0] = window

    print("=" * 60)
    print("🌿 V.E.R.D.A.N.T. Desktop Floating Capsule")
    print(f"   Native Frameless Window · Always On Top")
    print(f"   Position: ({WIN_X}, {WIN_Y})  Size: {WIN_W}x{COLLAPSED_H}")
    print("=" * 60)

    webview.start(debug=False)


if __name__ == "__main__":
    main()
