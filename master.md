# V.E.R.D.A.N.T. — Master Engineering & Strategy Blueprint
### Visual Entropy & Runtime Distillation for Autonomous Net-Reduction Testing
*Built for the Google Cloud & DeepMind Startup Buildathon India 2026*

---

## 1. Executive Summary & The Core Discovery

### The Problem
Engineering teams waste **40% of their sprints** manually reproducing bugs from vague user screen recordings, hand-writing brittle end-to-end tests, and burning cloud kilowatt-hours in failed CI loops. Meanwhile, existing AI test generation tools suffer from two fatal flaws:
1. **The Naive LLM Wrapper Trap:** Feeding raw 30-second video MP4s directly to LLMs results in severe hallucinations, missed micro-glitches, and token budget exhaustion.
2. **The Coordinate Clicker Trap:** Brittle pixel-clicking bots that break upon any minor window resize, font shift, or layout reflow.

### The Discovery: Forensic Triangulation with Dual-Engine Consensus
> **"Visuals show WHAT happened. Network and DOM logs show WHY it happened. Mathematical micro-diffing verifies WHERE it broke."**

V.E.R.D.A.N.T. unifies **Google Gemini 1.5 Pro's cognitive multimodal vision** with a **deterministic mathematical pixel sentinel** and an **event-driven DOM/network stream**, delivering **100% bug detection accuracy with zero hallucinations**, verified by a closed-loop **RED-to-GREEN automated test cycle**.

---

## 2. Complete End-to-End System Architecture

```mermaid
flowchart TD
    subgraph Ingestion ["1. Forensic Ingestion & Pre-Ingestion Sanitization"]
        V[30s Screen Recording MP4]
        HAR[Network HAR Logs - 4xx/5xx Errors]
        Logs[Browser Console Logs & Stack Traces]
        DOM[DOM MutationObserver Delta Stream]
        PII[PII Redactor: Obfuscate Passwords & Regex-Scrub Bearer Tokens]
    end

    subgraph ContextPrism ["2. ContextPrism (Intelligent Event Extractor)"]
        Anchor[Safety-Anchored Keyframe Isolator: ±1.5s around all user actions]
        Timeline[Structured Chronological JSON Timeline Builder]
        AST[Target Repo AST Pruner: Extract Only Related Interfaces & Handlers]
    end

    subgraph DualEngine ["3. Dual-Engine Forensic Analysis"]
        Gemini["🧠 Engine A: Google Gemini 1.5 Pro\n(Semantic Reasoning, User Intent, Structured JSON & Code Patch)"]
        Sentinel["⚙️ Engine B: Custom SSIM & DOM Sentinel\n(Mathematical Pixel Delta, Coordinate Snapping, DOM State Lock)"]
        Arbiter{"⚖️ 3-Tier Consensus Arbiter\n(Ground-Truth Hierarchy & Multi-Evidence Confidence Scoring)"}
    end

    subgraph ReplaySandbox ["4. Replay Shield & Verification Sandbox"]
        Docker[Sandboxed Headless Chromium Container]
        Phase1["Phase 1: Run Generated Playwright Test on Broken Code (RED ❌)"]
        Phase2["Phase 2: Apply Gemini's 3-Line Surgical Patch to Ephemeral Branch"]
        Phase3["Phase 3: Re-run Playwright Test on Patched Code (GREEN ✅)"]
        Phase4["Phase 4: Run Existing Regression Test Suite (Ensure 0 Side-Effects)"]
    end

    subgraph GreenTelemetry ["5. Scientific Green Analytics & GitHub Automation"]
        RAPL[Direct Machine Energy Profiler: Joules & CPU/GPU Time]
        CloudEst["Estimated Cloud Compute & Cooling Water Reduction (A/B Baseline)"]
        PR["Reviewer-Ready Draft Pull Request on Ephemeral Feature Branch"]
    end

    Ingestion --> PII --> Anchor --> Timeline --> DualEngine
    AST --> Gemini
    Gemini --> Arbiter
    Sentinel --> Arbiter
    Arbiter --> Docker
    Docker --> Phase1 --> Phase2 --> Phase3 --> Phase4
    Phase4 --> RAPL --> CloudEst --> PR
```

---

## 3. Deep-Dive: The Three Functional Layers

### Layer 1: ContextPrism (Intelligent Event Extractor)
Instead of acting as a generic video compressor, ContextPrism transforms raw unstructured video into a structured event-driven JSON schema:
* **Safety-Anchored Keyframe Isolation:** Computes structural similarity (SSIM). Frames with zero semantic change are dropped, but **safety anchors freeze and preserve all frames within $\pm 1.5\text{s}$ of any mouse click, network request failure, or DOM mutation**.
* **Zero-Copy Serialization Stream:** Decouples video extraction from analysis. Frames and DOM deltas stream directly into memory buffers without waiting for full video completion.
* **Chronological Action Timeline:** Produces an empirical timeline of user interactions:
  ```json
  {
    "session_duration_s": 24.2,
    "key_events": [
      {"timestamp": "00:04", "action": "NAVIGATE", "target": "https://app.store/cart"},
      {"timestamp": "00:11", "action": "CLICK", "selector": "#checkout-btn", "x": 640, "y": 820},
      {"timestamp": "00:12", "action": "NETWORK_FAIL", "endpoint": "/api/v1/checkout", "status": 500},
      {"timestamp": "00:14", "action": "UI_FREEZE", "state": "button_disabled_no_repaint"}
    ],
    "critical_keyframes": [11, 12, 14],
    "suspect_source_files": ["src/api/checkoutHandler.ts"]
  }
  ```
* **AST Scope Narrowing:** Parses the target GitHub repo's Abstract Syntax Tree (AST), targeting only functions and type contracts related to the failing endpoint, preventing full-repo token bloat.

---

### Layer 2: Dual-Engine Handshake & The Consensus Arbiter

| Component | Technology | Role |
| :--- | :--- | :--- |
| **Engine A (Semantic Brain)** | **Google Gemini 1.5 Pro** | Multimodal video understanding, cognitive user intent mapping, structured JSON output, and surgical code patch generation. |
| **Engine B (Deterministic Sentinel)** | **Custom SSIM & DOM Engine** | Mathematical pixel-delta calculation, bounding box clustering, DOM computed-style verification, and coordinate snapping. |
| **Consensus Arbiter** | **In-Memory State Machine (<10ms)** | Arbitrates discrepancies between Gemini and Engine B using a strict ground truth hierarchy. |

#### The 3-Tier Arbitration Hierarchy
1. **Rule 1 (Network & Console Logs are Absolute Truth):** If a network HAR records an HTTP `500` or the console captures an unhandled exception, technical failure overrules visual interpretations.
2. **Rule 2 (Pixel Delta Overrules "Visual Success"):** If Gemini claims an action succeeded, but Engine B detects $0\%$ pixel change and no DOM repaint within 500ms, the Arbiter flags a **"Silent UI Freeze"** defect.
3. **Rule 3 (Gemini Overrules Benign Visual Noise):** If Engine B flags a high pixel change $(>15\%)$ caused by a background video ad or loading spinner, Gemini inspects the DOM and discards the false alarm.

#### Multi-Evidence Confidence Scoring Formula
$$\text{Confidence Score} = w_1 S_{\text{visual}} + w_2 S_{\text{network}} + w_3 S_{\text{console}} + w_4 S_{\text{DOM}}$$
*Weights ($w_1=0.25, w_2=0.35, w_3=0.25, w_4=0.15$) reward cross-source agreement, giving developers an empirical reliability metric (e.g., `94% High Confidence`).*

---

### Layer 3: Replay Shield, Green Telemetry & GitHub Engine

#### 1. The Red-to-Green Replay Shield
* **Phase 1 (Prove the Bug):** ApexTrace compiles the timeline into a deterministic **Playwright script**. It executes inside a sandboxed headless Chromium container on the unpatched codebase. **The test MUST fail (RED ❌)**.
* **Phase 2 (Apply the Patch):** Gemini's proposed 3-line surgical fix is applied to a detached feature branch (`verdant/patch-issue-xxx`).
* **Phase 3 (Verify the Fix):** The exact Playwright script is re-executed. **The test MUST pass (GREEN ✅)**.
* **Phase 4 (Regression Guardrail):** The repo's existing test suite (`npm test` / `pytest`) is triggered to ensure zero broken side effects.

#### 2. Scientific Green Computing Analytics (A/B Baseline)
We reject unscientific claims like "net-zero". Instead, we compute **Estimated Net Resource Reduction** against a defined baseline:
* **Baseline A (Unoptimized):** Processing raw 30s 1080p video + whole-repo context through LLM + unguided test retries.
* **Optimized B (V.E.R.D.A.N.T.):** Targeted keyframe strips + AST-distilled context + single-shot deterministic Playwright run.
* **Mathematical Telemetry Formulas:**
  $$\Delta \text{Energy (Wh)} = \left(\text{Tokens}_{\text{saved}} \times 0.0004\text{ Wh}\right) + \Delta \text{Compute}_{\text{CPU/GPU}}$$
  $$\text{Estimated Cooling Water (ml)} = \Delta \text{Energy (kWh)} \times \text{PUE}_{\text{cloud}} \times \text{WUE}_{\text{cooling}} \times 1000$$
  *(Where $\text{PUE} \approx 1.1$ and $\text{WUE} \approx 1.8\text{ L/kWh}$ based on published Google Cloud data center averages).*

#### 3. Reviewer-Ready GitHub Draft PR
Opens an automated **Reviewer-Ready Draft Pull Request** containing:
* The failing-turned-passing Playwright reproduction script.
* The surgical code patch.
* Full Forensic Evidence Report (Timestamps, Network Traces, Console Stack).
* The **Green Computing Impact Badge** linking directly to the estimation methodology.

---

## 4. The 9 Addressed Bottlenecks & Defensive Mitigations

| # | Challenge | Root Risk | Concrete Architecture Guardrail |
| :- | :--- | :--- | :--- |
| **1** | **Screen Recording Ambiguity** | Video shows *what* broke, not *why*. | **Multimodal Triangulation:** Pair visual keyframes with browser console logs (`console.error`) and network HAR traces (`4xx/5xx`). |
| **2** | **Over-Pruning in ContextPrism** | Deleting duplicate frames might erase a tiny 1-line error banner. | **Safety Anchors:** Freeze and preserve all frames $\pm 1.5\text{s}$ around mouse clicks, API failures, or DOM mutations. |
| **3** | **Flaky Playwright Test Scripts** | Dynamic IDs, animations, and slow networks break tests. | **Self-Healing Selectors:** Prioritize user-facing accessibility roles (`getByRole`, `getByText`) over brittle CSS/XPath with auto-retry assertions. |
| **4** | **Unsafe Automated Code Fixes** | AI patch breaks another feature or hallucinates changes. | **Strict Sandbox Verification:** Run existing regression test suites in Docker *before* opening a PR. **Never auto-merge without human approval.** |
| **5** | **Resource Measurement Credibility** | Claiming literal "net-zero" invites immediate skepticism. | **Transparent Estimation Model:** Display standard formulas based on hardware RAPL/NVML + Google Cloud PUE/WUE. Label as *"Estimated Savings."* |
| **6** | **GitHub Integration & Rate Limits** | Repo structure mismatch, private repo auth, and rate limits. | **Ephemeral Feature Branches:** Always branch from `HEAD` (`verdant/bugfix-xxx`), generate standard unified `.diff`, and post via scoped GitHub App. |
| **7** | **Gemini API Costs & Limits** | High token usage and payload timeouts from raw videos. | **Pre-Flight Compression:** ContextPrism sends downsampled keyframe strips instead of raw video, keeping tokens well under budget. |
| **8** | **Security & PII in Screen Captures** | Passwords, auth tokens, or private data visible in screen video. | **Pre-Ingestion Redaction:** Black out password input coordinates and regex-scrub auth headers (`Bearer ...`) from network logs before AI ingestion. |
| **9** | **End-to-End Pipeline Fragility** | If 1 component hiccups, the entire demo fails. | **Graceful Degradation:** If Gemini test synthesis times out, the deterministic pixel watchdog still outputs visual diff timestamps and logs. |

---

## 5. Master Implementation Roadmap (4 Phases)

### Phase 1: ContextPrism & Forensic Ingestion (Days 1–3)
* Build Python FFmpeg pipeline to sample keyframes with $\pm 1.5\text{s}$ Safety Anchors.
* Implement PII scrubber: Regex-mask passwords, JWTs, and credit card patterns from network payloads and screenshot coordinates.
* Implement Zero-Copy asynchronous streaming buffer between ingestion and analysis.

### Phase 2: Dual-Engine Forensic Analysis & Consensus Arbiter (Days 4–6)
* Configure Google Gemini 1.5 Pro API with structured output schema (`response_mime_type: "application/json"`).
* Build lightweight Python SSIM + pixel-delta comparator with 360p downscaling and ROI cursor zoom.
* Implement in-memory 3-Tier Arbiter and weighted multi-evidence confidence scoring algorithm.

### Phase 3: Playwright Replay Shield & Surgical Patching (Days 7–9)
* Translate timeline steps into standard Playwright TypeScript code using accessibility locators.
* Configure Docker sandboxed Chromium runner to verify test failure (RED ❌) on original code.
* Feed target source file AST to Gemini to generate focused code diff; apply patch to branch.
* Re-run Playwright test to verify pass (GREEN ✅) and execute full test suite for zero regressions.

### Phase 4: Green Analytics Engine & GitHub Automation (Days 10–12)
* Implement A/B baseline compute telemetry: Wh energy delta and data center cooling water estimation.
* Build GitHub App bot to branch, commit, and open **Reviewer-Ready Draft Pull Request**.
* Assemble interactive live demo canvas for Buildathon presentation.

---

## 6. The 3-Minute Winning Demo Script for Google Judges

* **Minute 1: The Pain Point & The Drop (0:00 – 1:00)**  
  *"Every day, engineers waste 40% of their sprints watching screen recordings, trying to recreate bugs, and burning thousands of cloud kilowatt-hours in failed CI loops."*  
  *Action:* Drag and drop a real 30-second screen recording of an e-commerce checkout page where clicking *"Place Order"* silently hangs. ContextPrism isolates the 3 critical keyframes and 500 API drop in under 1 second.
* **Minute 2: The Forensic Replay & Sandbox Verification (1:00 – 2:00)**  
  Show the **94% Evidence-Backed Confidence Score** linking Visual freeze, DOM disabled state, and Network 500 error. Watch the Playwright test fail live in Docker (**RED ❌**), apply the 3-line patch, and pass cleanly (**GREEN ✅**) with all regression tests green.
* **Minute 3: The Reviewer-Ready PR & The Eco-Report (2:00 – 3:00)**  
  Switch to GitHub. A freshly opened **Reviewer-Ready Draft PR** is already live with the Playwright test, code patch, and Green Computing Savings Report showing **68% token compute** and **8.4 ml of data center cooling water saved**.  
  *Climax:* *"We don't just find bugs. We prove them, fix them, protect against regressions, and save cloud resources—with human approval always in the loop."*
