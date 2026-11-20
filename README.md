# 🌿 V.E.R.D.A.N.T. (v2.5)
### **Visual Entropy & Runtime Distillation for Autonomous Net-zero Testing**
*Built for the **Google Cloud & Google DeepMind: Startup Buildathon India 2026***

[![Google Cloud](https://img.shields.io/badge/Google%20Cloud-Run%20%7C%20Storage%20%7C%20Vertex%20AI-4285F4?logo=google-cloud&logoColor=white)](https://cloud.google.com/)
[![Google DeepMind](https://img.shields.io/badge/Google%20DeepMind-Gemini%203.1%20%26%203.5-34A853?logo=google&logoColor=white)](https://deepmind.google/)
[![Playwright](https://img.shields.io/badge/Testing-Playwright%20E2E-2EAD33?logo=playwright&logoColor=white)](https://playwright.dev/)
[![Chrome Extension](https://img.shields.io/badge/Chrome-Manifest%20v3-4285F4?logo=google-chrome&logoColor=white)](https://developer.chrome.com/docs/extensions/)
[![VS Code](https://img.shields.io/badge/IDE-VS%20Code%20Extension-007ACC?logo=visual-studio-code&logoColor=white)](https://code.visualstudio.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

> **One-Line Pitch:** A multi-surface autonomous debugging runtime: Catch both runtime crashes and silent visual UI formatting defects directly in Google Chrome, test synthesized hot-patches live in the browser tab, and stream verified atomic diffs with Playwright reproducers straight to VS Code in under 4 seconds — backed by Google Cloud Run and DeepMind Gemini.

---

## 📌 1. The Autonomous Multi-Surface Architecture

V.E.R.D.A.N.T. operates as a closed-loop engineering ecosystem connecting browser runtime, serverless cloud compute, and the developer IDE:

```
┌────────────────────────────────────────────────────────────────────────┐
│                        CHROME EXTENSION (v3)                           │
│  • Rolling 30s Console & Network Buffer (Zero CPU overhead)            │
│  • Visual Bug Element Inspector (BoundingBox, Computed CSS, Overflow)  │
│  • Client-Side Zero-Leakage PII Scrubber (Redacts JWTs, Keys, Cards)   │
│  • 🧪 In-Tab Hot-Patcher (Test CSS & API fixes live in active tab)     │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ HTTPS Ingest (~3.9s)
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│         CENTRAL CLOUD RUN DAEMON & STITCH PORTAL (FastAPI :8000)       │
│  • Multimodal Reasoning via Google DeepMind Gemini 3.1 & 3.5           │
│  • Double-Pass PII Sanitization & Zero-Data-Leakage Guarantee          │
│  • Persistent SQLite WAL / Cloud SQL Database with Fernet Encryption   │
│  • WebSocket Streaming Hub (/ws/ide)                                   │
│  • VERDE Eco Telemetry (-84.9% Token Bloat, 584 Wh & 1.18 L Saved)     │
└──────────────────┬─────────────────────────────────┬───────────────────┘
                   │                                 │
                   │ WebSocket (/ws/ide)             │ Headless E2E Specs
                   ▼                                 ▼
┌──────────────────────────────────────┐  ┌──────────────────────────────┐
│        VS CODE COMPANION IDE         │  │   AUTONOMOUS SENTINEL        │
│  • Auto-jump to suspect file & line  │  │   • Headless Chromium Crawler│
│  • Inline Git-style patch preview    │  │   • Closed-Loop Verification │
│  • 1-Click Patch Acceptance          │  │   • Automated Playwright Run │
└──────────────────────────────────────┘  └──────────────────────────────┘
```

---

## 🚀 2. Key Capabilities & Innovations

### A. Visual & Formatting Bug Detection (No Console Errors Required)
* **Geometry & Overflow Crawler**: Inspects `scrollWidth > clientWidth`, clipping, missing flex-shrink, and padding collisions using `getBoundingClientRect()`.
* **Gemini Layout Reasoning**: Synthesizes exact CSS rules (e.g. `.pricing-card h3 { overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }`).
* **Live In-Tab Hot Patching**: Apply and verify the fix inside the browser tab with one click before touching a single line of backend code.

### B. Enterprise Zero-Leakage PII Sanitization
* **Double-Layer Defense**: Scrubbed first on the client (browser JavaScript) and verified again on the server (Python daemon).
* **Redacted Targets**: Bearer JWTs, AWS Keys (`AKIA...`), GitHub PATs (`ghp_...`), Google API Keys (`AIza...`), passwords in URLs/JSON, credit cards, emails, and phone numbers.

### C. Persistent Audit Trail & Closed-Loop Verification
* **Encrypted Credential Storage**: Uses Fernet AES cryptography at rest for GitHub tokens and secrets.
* **Incident Ledger**: Stores session audit trails, generated reproduction steps, carbon/water conservation metrics, and PR URLs.

### D. Google Cloud Native & Net-Zero Carbon Alignment
* **Pinned Green Grid**: Default deployment to Google Cloud region `us-central1` (Iowa datacenter running on **92% Carbon Free Energy [CFE%]** with PUE 1.10).
* **Scale-to-Zero Compute**: Powered by Google Cloud Run with 0 idle CPU watts.

---

## 💻 3. Quickstart Guide

### 1. Run Locally (FastAPI Central Portal)
```bash
# Clone the repository
git clone https://github.com/dhairya-shah7/VERDANT.git
cd VERDANT

# Install dependencies
pip install -r requirements.txt

# Start Daemon Server & Central Portal
python server.py
# Central Portal & Dashboard running on http://localhost:8000
```

### 2. Deploy to Google Cloud Run (One-Click)
Ensure you have the [Google Cloud CLI (`gcloud`)](https://cloud.google.com/sdk/docs/install) installed and logged in:

```powershell
# Windows (PowerShell)
powershell -ExecutionPolicy Bypass -File .\deploy_gcp.ps1
```

```bash
# Linux / macOS / Google Cloud Shell
chmod +x deploy_gcp.sh
./deploy_gcp.sh
```

### 3. Install the Chrome Extension (`verdant-chrome`)
1. Open Google Chrome $\to$ navigate to `chrome://extensions`.
2. Toggle **"Developer mode"** ON (top-right).
3. Click **"Load unpacked"** $\to$ select the `verdant-chrome` folder.
4. Pin the green **V.E.R.D.A.N.T. 🌱** icon to your toolbar.
5. On any webpage:
   - Click **"🔍 Inspect Element"** to diagnose layout bugs, or browse normally to auto-detect exceptions.
   - Click **"🧪 Test Fix Live in Tab"** to preview the CSS fix in real time.
   - Click **"💻 Send to VS Code"** to stream the patch to your IDE.

### 4. Install the VS Code Extension (`verdant-vscode`)
1. Copy or symlink `verdant-vscode` to your extensions directory (`~/.vscode/extensions/verdant-vscode` or `%USERPROFILE%\.vscode\extensions\verdant-vscode`).
2. Reload VS Code.
3. The status bar will show: `$(beaker) V.E.R.D.A.N.T.: Connected (:8000)`.
4. When Chrome sends a bug, VS Code automatically opens the suspect file, highlights the line, renders the diff, and lets you accept the patch or run the Playwright test.

---

## 📁 4. Repository Structure

```
VERDANT/
├── verdant-chrome/             # Manifest v3 Chrome Extension (Capture & Hot-Patcher)
│   ├── manifest.json           # Extension manifest (MV3 permissions)
│   ├── background.js           # Service worker & tab screenshot engine
│   ├── content.js              # DOM error listeners & drawer injector
│   ├── drawer.js & drawer.css  # Sliding debugger drawer UI
│   ├── popup/                  # Toolbar popup UI
│   └── src/
│       ├── pii_scrubber.js     # Client-side zero-leakage secret scrubber
│       ├── visual_crawler.js   # Element geometry & layout bug inspector
│       └── in_tab_patcher.js   # In-browser CSS hot-patch injector
├── verdant-vscode/             # VS Code IDE Companion Extension
│   ├── package.json            # Extension manifest & commands
│   └── extension.js            # WebSocket client, file jumper, & patch runner
├── verdant-sentinel/           # Autonomous Headless Chromium QA Crawler
├── src/                        # Core Python Engine
│   ├── context_prism/          # PII sanitizer, log parsers, & AST skeletonizer
│   ├── dual_engine/            # Gemini analyzer & SSIM Sentinel
│   ├── replay_shield/          # Playwright reproduction test generator
│   ├── verde_telemetry/        # Eco telemetry & GitHub PR reporter
│   ├── db/                     # Encrypted SQLite WAL audit engine & persistence
│   ├── gcp_adapter.py          # Google Cloud Vertex AI, GCS, & Cloud SQL adapter
│   └── stitch_template.py      # Embedded Central Portal single-page application
├── tests/                      # Automated Verification Test Suite
├── Dockerfile                  # Production Multi-Stage Google Cloud Run Container
├── cloudbuild.yaml             # Google Cloud Build CI/CD Automation Pipeline
├── deploy_gcp.ps1              # Windows One-Click Cloud Run Deployer
├── deploy_gcp.sh               # Linux/macOS One-Click Cloud Run Deployer
├── GCP_SETUP_GUIDE.md          # Comprehensive Google Cloud Architecture Guide
├── requirements.txt            # Core Production Dependencies
└── README.md                   # System documentation
```

---

## 👥 5. Team & Attribution
**Team MaDrix**  
*Built for the Google Cloud & Google DeepMind Startup Buildathon India 2026.*  
Licensed under the [MIT License](LICENSE).
