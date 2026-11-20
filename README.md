# 🌿 V.E.R.D.A.N.T. (v2.4)
### **Visual Entropy & Runtime Distillation for Autonomous Net-zero Testing**
*Built for the **Google Cloud & Google DeepMind: Startup Buildathon India 2026***

[![Google Cloud](https://img.shields.io/badge/Google%20Cloud-Run%20%7C%20Storage-4285F4?logo=google-cloud&logoColor=white)](https://cloud.google.com/)
[![Google DeepMind](https://img.shields.io/badge/Google%20DeepMind-Gemini%203.1%20Flash--Lite-34A853?logo=google&logoColor=white)](https://deepmind.google/)
[![Playwright](https://img.shields.io/badge/Testing-Playwright%20E2E-2EAD33?logo=playwright&logoColor=white)](https://playwright.dev/)
[![Chrome Extension](https://img.shields.io/badge/Chrome-Manifest%20v3-4285F4?logo=google-chrome&logoColor=white)](https://developer.chrome.com/docs/extensions/)
[![VS Code](https://img.shields.io/badge/IDE-VS%20Code%20Extension-007ACC?logo=visual-studio-code&logoColor=white)](https://code.visualstudio.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

> **One-Line Pitch:** A multi-surface autonomous debugging runtime: Catch both runtime crashes and silent visual UI formatting defects directly in Google Chrome, test synthesized hot-patches live in the browser tab, and push verified atomic diffs with Playwright reproducers straight to VS Code in under 4 seconds.

---

## 📌 1. The Autonomous Ecosystem

V.E.R.D.A.N.T. has evolved beyond a manual upload portal into a unified, multi-surface engineering toolchain:

```
┌────────────────────────────────────────────────────────────────────────┐
│                        CHROME EXTENSION (v3)                           │
│  • Rolling 30s Console & Network Buffer (Zero CPU overhead)            │
│  • Visual Bug Element Inspector (BoundingBox, Computed CSS, Overflow)  │
│  • Client-Side Zero-Leakage PII Scrubber (Redacts JWTs, Keys, Cards)   │
│  • 🧪 In-Tab Hot-Patcher (Test CSS & API fixes live in active tab)     │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ POST /api/extension/ingest (~3.9s)
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                   LOCAL BRIDGE DAEMON (FastAPI :8000)                  │
│  • Multimodal Diagnostics via Google Gemini 3.1 Flash-Lite             │
│  • Server-Side Double-Pass PII Sanitization                            │
│  • WebSocket Streaming Hub (/ws/ide)                                   │
│  • VERDE Eco Telemetry (-84.9% Token Bloat, 584 Wh & 1.18 L Saved)     │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ WebSocket Event Broadcast (/ws/ide)
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                         VS CODE IDE EXTENSION                          │
│  • Auto-Focus: Jumps directly to suspect source file and line number   │
│  • Inline Diff Review: Git-style search/replace patch preview          │
│  • 1-Click Patch Acceptance & File Writing                             │
│  • Playwright Test Runner: Headed execution of generated .spec.ts      │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 🚀 2. Core Capabilities

### A. Visual & Formatting Bug Detection (No Console Errors Required)
- **Geometry & Overflow Crawler**: Inspects `scrollWidth > clientWidth`, clipping, missing flex-shrink, and padding collisions using `getBoundingClientRect()`.
- **Gemini 3.1 Multimodal Layout Reasoning**: Synthesizes exact CSS rules (e.g. `.pricing-card h3 { overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }`).
- **Live In-Tab Hot Patching**: Apply and verify the fix inside the browser tab with one click before touching a single line of backend code.

### B. Enterprise Zero-Leakage PII Sanitization
- **Double-Layer Defense**: Scrubbed first on the client (browser JavaScript) and verified again on the server (Python daemon).
- **Redacted Targets**: Bearer JWTs, AWS Keys (`AKIA...`), GitHub PATs (`ghp_...`), Google API Keys (`AIza...`), passwords in URLs/JSON, credit cards, emails, and phone numbers.

### C. Lightning Fast Multimodal Reasoning
- Powered by `gemini-3.1-flash-lite` for **~2–4 second dynamic inference** with zero hardcoded scenario templates.

---

## 💻 3. Quickstart Guide

### 1. Start the Local Bridge Daemon
```bash
# Clone the repository
git clone https://github.com/dhairya-shah7/VERDANT.git
cd VERDANT

# Install dependencies
pip install -r requirements.txt

# Start Daemon Server
python server.py
# Running on http://localhost:8000
```

### 2. Install the Chrome Extension (`verdant-chrome`)
1. Open Google Chrome $\to$ navigate to `chrome://extensions`.
2. Toggle **"Developer mode"** ON (top-right).
3. Click **"Load unpacked"** $\to$ select the `verdant-chrome` folder.
4. Pin the green **V.E.R.D.A.N.T. 🌱** icon to your toolbar.
5. Open any webpage:
   - Click the floating green pill or popup menu.
   - Click **"🔍 Inspect Element"** to diagnose layout bugs, or browse normally to auto-detect exceptions.
   - Click **"🧪 Test Fix Live in Tab"** to preview the fix instantly.
   - Click **"💻 Send to VS Code"** to push to your IDE.

### 3. Install the VS Code Extension (`verdant-vscode`)
1. Link or copy `verdant-vscode` to your VS Code extensions folder (`~/.vscode/extensions/verdant-vscode` or `%USERPROFILE%\.vscode\extensions\verdant-vscode`).
2. Reload VS Code.
3. The status bar displays: `$(beaker) V.E.R.D.A.N.T.: Connected (:8000)`.
4. When Chrome sends a bug, VS Code automatically opens the file, highlights the suspect line, renders the diff, and lets you run the Playwright test.

---

## 📁 4. Repository Structure

```
VERDANT/
├── verdant-chrome/             # Manifest v3 Chrome Extension
│   ├── manifest.json           # Extension manifest (permissions & resources)
│   ├── background.js           # Service worker & tab screenshot engine
│   ├── content.js              # Error listeners & DOM injection
│   ├── drawer.js & drawer.css  # Sliding debugger drawer component
│   ├── popup/                  # Toolbar popup UI
│   └── src/
│       ├── pii_scrubber.js     # Client-side zero-leakage secret scrubber
│       ├── visual_crawler.js   # Element geometry & layout bug inspector
│       └── in_tab_patcher.js   # In-browser CSS hot-patch injector
├── verdant-vscode/             # VS Code IDE Companion Extension
│   ├── package.json            # Extension manifest & commands
│   └── extension.js            # WebSocket client, file jumper, & patch runner
├── src/                        # Core Python Engine
│   ├── context_prism/          # Layer 1: PII sanitizer & AST skeletonizer
│   ├── dual_engine/            # Layer 2: Gemini 3.1 & SSIM Sentinel
│   ├── replay_shield/          # Layer 3: Playwright test generator
│   └── verde_telemetry/        # Layer 4: Compute meter & GitHub reporter
├── tests/                      # Automated Verification Test Suite
│   ├── test_pii.py             # Enterprise PII redactor unit tests
│   ├── test_extension_api.py   # Live Gemini 3.1 Flash-Lite ingestion test
│   ├── test_ws.py              # WebSocket hub verification
│   └── test_e2e_ecosystem.py   # End-to-end Chrome -> Daemon -> VS Code test
├── server.py                   # FastAPI Local Bridge Daemon & Web Dashboard
├── requirements.txt            # Python dependencies
└── README.md                   # System documentation
```

---

## 👥 5. Team & Attribution
**Team MaDrix**  
*Built for the Google Cloud & Google DeepMind Startup Buildathon India 2026.*  
Licensed under the [MIT License](LICENSE).
