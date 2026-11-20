# V.E.R.D.A.N.T. — Master Implementation & Buildathon Roadmap
### Visual Entropy & Runtime Distillation for Autonomous Net-zero Testing
*Official Project Plan for Startup Buildathon India 2026 (Google Cloud & Google DeepMind)*

> [!IMPORTANT]
> **Core Architectural Mandate: Zero Pre-Made or Hardcoded Algorithms**
> - **Zero black-box bloat**: No heavy external frameworks (no OpenCV, LangChain, LlamaIndex, or third-party profilers).
> - **100% Bespoke Algorithms**: We build our own Entropy Frame-Diff Extractor, V-Token AST Skeletonizer, Thermodynamic Water/Energy Profiler, and Deterministic Unified Patch Generator from scratch.
> - **Hardware Decompression Stream**: Standard stdout pipe (`ffmpeg rawvideo`) feeds raw byte buffers directly to our custom Python algorithms, avoiding heavy C++ Python wrapper wheels.

---

## 1. System Overview & The Three Fused Pillars

```
       [ 30s Bug Video (MP4/WebM) + Console Logs via GitHub Issue or Web UI ]
                                       │
                                       ▼
  ═══════════════════════ PILLAR 1: CONTEXTPRISM ═══════════════════════
  * Custom V-Token AST Skeletonizer & DOM Pruner
  * Strips non-semantic filler, reducing context by 75% to 85% natively
  * Streams ultra-dense, low-latency payload to Google Gemini 1.5 Pro
                                       │
                                       ▼
  ════════════════════════ PILLAR 2: APEXTRACE ═════════════════════════
  * Gemini 1.5 Pro Multimodal Vision & State-Transition Engine
  * Reconstructs user click sequence, routing exceptions, and visual breaks
  * Synthesizes deterministic, executable Playwright / PyTest E2E scripts
                                       │
                                       ▼
  ═══════════════════════ PILLAR 3: VERDE-HYDRA ════════════════════════
  * Dynamic Compute Arbiter (GPU-to-CPU Thermal Offloading)
  * Bare-metal measurement of Water Cooling (ml), Joules, and Carbon (gCO2e)
  * Generates Verified Eco-Audit Badge on the Pull Request
```

---

## 2. Flagship Usability Features

### Feature 1: GitHub Issue-to-PR Auto-Pilot
1. A tester or user creates a GitHub issue and attaches a 30-second screen-recording MP4 showing a bug.
2. The **V.E.R.D.A.N.T. GitHub Action** triggers automatically.
3. It pipes video bytes into our **Native Entropy Frame-Diff Algorithm**, isolates the exact bug keyframe, and generates an executable Playwright test script.
4. It automatically opens a ready-to-merge Pull Request with:
   - The failing test script (proving the bug).
   - The proposed code patch.
   - An **Eco-Audit Badge** displaying exact milliliters of cooling water and Joules saved.

### Feature 2: Interactive Time-Travel Scrubbing Canvas
- In the Next.js developer dashboard, dragging the video scrubber across the timeline displays three synchronized panels:
  - The exact video frame.
  - The skeletonized AST code responsible for that UI component.
  - Live meters showing real-time **water cooling (ml), Joules, and Scope 2 carbon ($gCO_2e$)**.

### Feature 3: Thermodynamic Eco-Scheduler
- Dynamically recommends the greenest Google Cloud data center region and time of day (based on ambient wet-bulb temperature and carbon intensity) to run heavy regression test suites with **near-zero evaporative water cooling**.

---

## 3. Four-Phase Buildathon Execution Plan (Nov 8 – Dec 2)

| Phase | Milestone | Key Deliverables |
| :--- | :--- | :--- |
| **Phase 1 (Nov 8 – 13)** | **Application & Core Engine** | - Scaffolding in `Desktop/Buildathon`<br>- Custom AST skeletonizer (`verde_ast.py`)<br>- Video pipe + custom entropy frame differencer (`verde_diff.py`)<br>- 1-Page Pitch Deck for `startupbuildathon.com` |
| **Phase 2 (Nov 14 – 19)** | **Playwright & Eco-Telemetry** | - Structured prompt harness for Gemini 1.5 Pro<br>- Playwright Python test generator<br>- Bare-metal energy & water cooling thermodynamic formula integration |
| **Phase 3 (Nov 20 – 21)** | **City Buildathon Sprint** | - Working GitHub Action (Issue-to-PR Auto-Pilot)<br>- Next.js Interactive Time-Travel Cockpit<br>- Live demo with real bug video |
| **Phase 4 (Nov 22 – Dec 02)** | **Grand Finale at Google BLR** | - Final benchmark reports (Token compression % and Liters of water saved)<br>- Pitch deck presentation for Google DeepMind & Google Cloud VCs |

---

## 4. Directory Structure
```
Desktop/Buildathon/
├── MASTER_PLAN.md               # Master specification & roadmap (This file)
├── IMPLEMENTATION_PLAN.md        # Technical architecture details
├── CUSTOM_ENGINE_SPEC.md        # Mathematical & algorithmic definitions
├── src/
│   ├── frame_diff.py            # Bespoke entropy frame-diff algorithm
│   ├── ast_skeletonizer.py      # Bespoke Python/TS syntax tree pruner
│   ├── patch_engine.py          # Unified diff & Playwright generator
│   └── telemetry.py             # Bare-metal energy & water profiler
└── action/                      # GitHub Issue-to-PR Action workflow
```
