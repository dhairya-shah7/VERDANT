# V.E.R.D.A.N.T. Autonomous Chrome Extension

Autonomous in-browser defect detection, visual element layout debugging, client-side PII scrubbing, and instant live hot-patching.

## Quick Installation (30 Seconds)
1. Open Google Chrome and go to `chrome://extensions/`.
2. Turn ON **Developer mode** (toggle in the top-right corner).
3. Click **Load unpacked**.
4. Select the `verdant-chrome` folder in this repository.
5. Pin the **V.E.R.D.A.N.T. 🌱** icon to your Chrome toolbar.

## Features
- **Client-Side Zero-Leakage PII Scrubbing**: Strips Bearer JWTs, passwords, API keys, and sensitive data *before* leaving the browser tab.
- **Visual & Layout Bug Inspector**: Click the floating green pill or `Inspect Element` crosshair on any broken component (e.g., text overflow, padding break, flexbox clipping) to capture geometry and computed CSS.
- **Automatic Crash & Exception Sniffer**: Detects unhandled JavaScript exceptions and HTTP 4xx/5xx network drops in real-time.
- **🧪 Test Fix Live**: Hot-patches CSS or mocks failing APIs directly inside the active tab.
- **💻 Send to VS Code**: Pushes defect locus, atomic diff, and Playwright test to your IDE in 1-click.
