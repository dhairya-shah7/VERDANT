# 🌿 V.E.R.D.A.N.T. Desktop Floating Capsule (`capsule/`)
**Visual Entropy & Runtime Distillation for Autonomous Net-zero Testing**
*Google Cloud & Google DeepMind — Startup Buildathon India 2026*

---

## Overview

The **Desktop Floating Capsule** is a lightweight, frameless, always-on-top desktop widget designed specifically for developers, QA engineers, and testers. Directly powered by **Google Gemini Multimodal Vision & Reasoning** (`gemini-3.5-flash` and `gemini-3.5-flash-lite`), it operates at the operating system layer to perceive bugs across your entire desktop environment.

```
┌────────────────────────────────────────────────────────────────────────┐
│  | Ask anything... (e.g. 'Fix the cart bug' or 'Explain this warning')  │
│  [+]  [🌿 Normal]  [💡 DeepThink]                 [🎙️ Voice]  [ ➤ ]     │
└────────────────────────────────────────────────────────────────────────┘
                                   │
              (Slide-out diff drawer when fix is detected)
                                   ▼
┌────────────────────────────────────────────────────────────────────────┐
│  Surgical Fix: src/components/Checkout.tsx (Confidence: 98%)           │
│  Spoken Brief: Added safety check before dereferencing paymentToken    │
│  ───────────────────────────────────────────────────────────────────── │
│  - if (cart.items.length && !isProcessing)                             │
│  + if (cart.items.length && !isProcessing && paymentToken)             │
│                                                                        │
│  [ ▶ Apply Patch & Run Verification Proof ]         [ ✕ Dismiss ]      │
└────────────────────────────────────────────────────────────────────────┘
```

---

## Key Features

1. **Active Window Snapper (`+` button)**:
   - Uses native Windows `win32gui` and `PIL` to cleanly capture the focused window (VS Code, Chrome, Postman, Terminal, Android Emulator) with zero window clutter.
2. **Dual Model Modes**:
   - **`🌿 Normal`**: Powered by `gemini-3.5-flash-lite` for ultra-low latency (<1s) answers.
   - **`💡 DeepThink`**: Powered by `gemini-3.5-flash` for multi-file AST reasoning and complex fixes.
3. **Push-to-Talk Voice (`🎙️ Voice`)**:
   - Streams 16kHz audio from your microphone directly to Gemini multimodal models.
4. **Slide-Out Surgical Diff Drawer**:
   - Replaces fragile diffs with atomic search/replace (`patcher.py`).
   - One-click `[ Apply Patch & Run Verification Proof ]` validates the change and prepares a verified GitOps PR payload.
5. **Global Hotkey (`Ctrl + Shift + Space`)**:
   - Instantly show/hide the capsule from anywhere in Windows.

---

## How to Run

From the project root:
```bash
python capsule/app.py
```
Or as a module:
```bash
python -m capsule.app
```
