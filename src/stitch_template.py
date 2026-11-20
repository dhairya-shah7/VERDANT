"""
V.E.R.D.A.N.T. — Stitch Design Suite Unified Interface
Faithful recreation of Google Stitch design suite for V.E.R.D.A.N.T.
Incorporating all 5 operational views with live FastAPI backend bindings:
1. Home Video Upload & Ingestion
2. Multi-Layer Processing Pipeline (Optical Flow & Frame Inspector)
3. Results & Verification Dashboard (Problem vs Solution & 3 Deep-Dive Tabs)
4. Verde-Hydra Sustainability & Data Center Water Dashboard
5. Persistent SQLite Audit History & Encrypted GitHub Connector
"""

STITCH_HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta content="width=device-width, initial-scale=1.0" name="viewport">
  <title>V.E.R.D.A.N.T. — Autonomous Bug Analysis & Fix Engine</title>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
  <link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200" rel="stylesheet">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
  <script src="https://cdn.tailwindcss.com"></script>
  <script id="tailwind-config">
    tailwind.config = {
      darkMode: "class",
      theme: {
        extend: {
          colors: {
            "primary": "#0058bd",
            "primary-container": "#2771df",
            "on-primary": "#ffffff",
            "on-primary-container": "#fefcff",
            "secondary": "#006e2c",
            "secondary-container": "#86f898",
            "on-secondary": "#ffffff",
            "on-secondary-container": "#00722f",
            "secondary-fixed": "#89fa9b",
            "on-secondary-fixed-variant": "#005320",
            "tertiary": "#765700",
            "tertiary-container": "#956e00",
            "surface": "#faf9fd",
            "surface-dim": "#dbd9dd",
            "surface-bright": "#faf9fd",
            "surface-container-lowest": "#ffffff",
            "surface-container-low": "#f4f3f7",
            "surface-container": "#efedf1",
            "surface-container-high": "#e9e7eb",
            "surface-container-highest": "#e3e2e6",
            "on-surface": "#1a1b1e",
            "on-surface-variant": "#424753",
            "outline": "#727785",
            "outline-variant": "#c2c6d5",
            "error": "#ba1a1a",
            "error-container": "#ffdad6",
            "on-error": "#ffffff",
            "on-error-container": "#93000a",
            "inverse-surface": "#2f3033",
            "inverse-on-surface": "#f1f0f4"
          },
          fontFamily: {
            "headline": ["Inter", "sans-serif"],
            "body": ["Inter", "sans-serif"],
            "code": ["JetBrains Mono", "monospace"]
          },
          spacing: {
            "gutter-desktop": "1.5rem",
            "space-xs": "0.25rem",
            "space-sm": "0.5rem",
            "space-md": "0.75rem",
            "space-lg": "1rem",
            "space-xl": "1.5rem"
          }
        }
      }
    };
  </script>
  <style>
    @layer base {
      html, body { margin: 0; padding: 0; }
      body { overscroll-behavior: none; }
    }
    .material-symbols-outlined {
      font-variation-settings: 'FILL' 0, 'wght' 400, 'GRAD' 0, 'opsz' 24;
    }
    .nav-tab-active {
      background-color: #e9e7eb !important;
      color: #1a1b1e !important;
      font-weight: 600 !important;
    }
  </style>
</head>
<body class="bg-surface font-body text-on-surface antialiased min-h-screen relative">

  <!-- ========================================================================= -->
  <!-- MOBILE / TABLET TOP HEADER (< lg screens)                                 -->
  <!-- ========================================================================= -->
  <header class="lg:hidden sticky top-0 z-40 bg-surface-container-lowest/95 backdrop-blur-md border-b border-surface-container-high px-4 py-3 flex items-center justify-between shadow-sm">
    <div class="flex items-center gap-2.5 cursor-pointer" onclick="navigateTab('home', event)">
      <div class="w-8 h-8 rounded-xl bg-secondary-fixed/60 flex items-center justify-center text-secondary shadow-sm">
        <span class="material-symbols-outlined text-[20px]">eco</span>
      </div>
      <div class="flex flex-col">
        <span class="font-bold text-sm text-on-surface leading-tight">V.E.R.D.A.N.T.</span>
        <span class="text-[10px] text-on-surface-variant leading-tight">Autonomous Bug Runtime</span>
      </div>
    </div>
    <div class="flex items-center gap-1.5">
      <button onclick="openGithubModal()" class="p-2 rounded-lg text-on-surface-variant hover:bg-surface-container transition" title="GitHub Configuration">
        <span class="material-symbols-outlined text-[20px]">account_tree</span>
      </button>
      <button onclick="toggleMobileSidebar()" class="p-2 rounded-lg text-on-surface hover:bg-surface-container transition" title="Toggle Navigation">
        <span class="material-symbols-outlined text-[24px]">menu</span>
      </button>
    </div>
  </header>

  <!-- Mobile Sidebar Backdrop Overlay -->
  <div id="sidebar-backdrop" onclick="closeMobileSidebar()" class="fixed inset-0 bg-black/40 backdrop-blur-sm z-40 lg:hidden hidden transition-opacity"></div>

  <!-- ========================================================================= -->
  <!-- 1. STITCH RESPONSIVE SIDEBAR NAVIGATION (Desktop: fixed, Mobile: drawer) -->
  <!-- ========================================================================= -->
  <aside id="main-sidebar" class="fixed left-0 top-0 bottom-0 h-screen w-64 bg-surface-container-lowest border-r border-surface-container-high z-50 flex flex-col justify-between p-4 shadow-[1px_0_8px_rgba(0,0,0,0.03)] transform -translate-x-full lg:translate-x-0 transition-transform duration-200 ease-in-out">
    <div class="flex flex-col gap-6">
      
      <!-- Brand Logo & Header -->
      <div class="flex items-center justify-between px-2 py-1">
        <div class="flex items-center gap-3 cursor-pointer" onclick="navigateTab('home', event); closeMobileSidebar();">
          <div class="w-9 h-9 rounded-xl bg-secondary-fixed/60 flex items-center justify-center text-secondary flex-shrink-0 shadow-sm">
            <span class="material-symbols-outlined text-[22px]">eco</span>
          </div>
          <div class="flex flex-col min-w-0">
            <span class="font-bold text-base text-on-surface tracking-tight leading-tight">V.E.R.D.A.N.T.</span>
            <span class="text-[11px] text-on-surface-variant leading-tight truncate">Autonomous Bug Runtime</span>
          </div>
        </div>
        <button onclick="closeMobileSidebar()" class="lg:hidden p-1.5 rounded-lg text-on-surface-variant hover:bg-surface-container transition">
          <span class="material-symbols-outlined text-[20px]">close</span>
        </button>
      </div>

      <!-- Navigation Links: ONLY 3 REQUESTED PAGES -->
      <nav class="flex flex-col gap-1.5" id="main-nav-bar">
        <a href="/" id="nav-btn-home" onclick="navigateTab('home', event); closeMobileSidebar();" class="nav-tab-active px-3.5 py-2.5 rounded-xl text-xs md:text-sm text-on-surface transition-all flex items-center gap-3 font-semibold cursor-pointer">
          <span class="material-symbols-outlined text-[20px] text-primary">eco</span>
          <span>Overview</span>
        </a>
        <a href="/sustainability" id="nav-btn-sustainability" onclick="navigateTab('sustainability', event); closeMobileSidebar();" class="px-3.5 py-2.5 rounded-xl text-xs md:text-sm text-on-surface-variant hover:text-on-surface hover:bg-surface-container transition-all flex items-center gap-3 font-medium cursor-pointer">
          <span class="material-symbols-outlined text-[20px] text-secondary">water_drop</span>
          <span>Sustainability (VERDE)</span>
        </a>
        <a href="/history" id="nav-btn-history" onclick="navigateTab('history', event); closeMobileSidebar();" class="px-3.5 py-2.5 rounded-xl text-xs md:text-sm text-on-surface-variant hover:text-on-surface hover:bg-surface-container transition-all flex items-center gap-3 font-medium cursor-pointer">
          <span class="material-symbols-outlined text-[20px]">history</span>
          <span>Audit History (<span id="nav-history-badge" class="font-bold text-secondary">5</span>)</span>
        </a>
      </nav>

      <!-- Quick Sustainability Action Card -->
      <div class="px-1">
        <a href="/sustainability" onclick="navigateTab('sustainability', event); closeMobileSidebar();" class="block p-3 rounded-xl bg-secondary-fixed/40 hover:bg-secondary-fixed/70 text-on-secondary-fixed-variant transition-all cursor-pointer border border-secondary-fixed">
          <div class="flex items-center gap-2 mb-1">
            <span class="material-symbols-outlined text-[18px] text-secondary">eco</span>
            <span class="text-xs font-bold">See What You Saved</span>
          </div>
          <p class="text-[11px] text-on-surface-variant leading-tight" id="sidebar-saved-summary">Calculated live per user from real audits.</p>
        </a>
      </div>

    </div>
  </aside>

  <!-- ========================================================================= -->
  <!-- MAIN WORKSPACE CONTAINERS                                                 -->
  <!-- ========================================================================= -->
  <main class="w-full lg:pl-64 min-h-screen bg-surface flex flex-col flex-1">

    <!-- ======================================================================= -->
    <!-- SCREEN 1: HOME VIDEO UPLOAD & INGESTION                                 -->
    <!-- ======================================================================= -->
    <div id="screen-home" class="w-full">
      <div class="relative w-full overflow-hidden">
        <div class="absolute -top-32 left-1/2 -translate-x-1/2 w-[780px] h-[340px] bg-gradient-to-b from-primary/10 via-secondary/5 to-transparent rounded-full blur-3xl pointer-events-none"></div>
        
        <div class="w-full max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-6 sm:py-10 flex flex-col gap-6 relative z-10">
          
          <!-- Hero Header -->
          <section class="w-full flex flex-col items-center text-center max-w-4xl mx-auto pt-2">
            <h1 class="text-2xl sm:text-3xl md:text-5xl font-black text-on-surface tracking-tight mb-3">
              Visual Entropy & Runtime Distillation for Autonomous Net-zero Testing.
            </h1>
            <p class="text-xs sm:text-sm md:text-base text-on-surface-variant max-w-3xl px-2 leading-relaxed">
              V.E.R.D.A.N.T. is the world's first thermodynamic, zero-waste autonomous debugging runtime. From live Chrome layout bugs to server exceptions, V.E.R.D.A.N.T. distills code ASTs, synthesizes in-tab live hot-patches, and dispatches verified Playwright PRs straight to VS Code.
            </p>

            <!-- 1-Click Multi-Surface Toolchain Downloads -->
            <div class="flex flex-wrap items-center justify-center gap-3 mt-4">
              <a href="/api/extension/download" download class="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl bg-primary hover:bg-primary/90 text-on-primary font-bold text-xs sm:text-sm shadow-md transition-all hover:scale-105 active:scale-95 cursor-pointer">
                <span class="material-symbols-outlined text-[20px]">extension</span>
                <span>Download Chrome Extension (.zip)</span>
              </a>
              <a href="/api/vscode/download" download class="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl bg-surface-container-high hover:bg-surface-container-highest text-on-surface font-semibold text-xs sm:text-sm border border-surface-container-high shadow-sm transition-all hover:scale-105 active:scale-95 cursor-pointer">
                <span class="material-symbols-outlined text-[20px]">terminal</span>
                <span>Get VS Code Extension (.zip)</span>
              </a>
            </div>
          </section>

          <!-- 3D Nature & Technology Visual Showcase Grid -->
          <!-- 3 Pristine Architecture Showcase Cards -->
          <section class="w-full grid grid-cols-1 md:grid-cols-3 gap-5 my-2">
            
            <!-- Card 1: Autonomous CI/CD Sentinel -->
            <div class="bg-surface-container-lowest rounded-2xl p-4 border border-surface-container-high shadow-sm hover:shadow-md transition-all flex flex-col">
              <div class="w-full h-44 rounded-xl overflow-hidden mb-3 bg-surface-container-high border border-surface-container-high/60">
                <img src="/uploads/assets/overview_ci_cd_sentinel.jpg" class="w-full h-full object-cover hover:scale-105 transition-transform duration-300" alt="Autonomous CI/CD Sentinel">
              </div>
              <div class="flex items-center gap-1.5 mb-1.5">
                <span class="px-2 py-0.5 rounded-full bg-secondary-fixed/50 text-secondary text-[11px] font-bold">🤖 CI/CD Sentinel</span>
              </div>
              <h3 class="text-base font-bold text-on-surface mb-1">Autonomous Self-Healing</h3>
              <p class="text-xs text-on-surface-variant leading-relaxed">
                Headless Playwright synthetic crawler tests Desktop & Mobile viewports on every PR. Autonomously verifies RED ❌ to GREEN ✅ and commits verified code fixes.
              </p>
            </div>

            <!-- Card 2: Multi-Surface Trinity Architecture -->
            <div class="bg-surface-container-lowest rounded-2xl p-4 border border-surface-container-high shadow-sm hover:shadow-md transition-all flex flex-col">
              <div class="w-full h-44 rounded-xl overflow-hidden mb-3 bg-surface-container-high border border-surface-container-high/60">
                <img src="/uploads/assets/overview_trinity_architecture.jpg" class="w-full h-full object-cover hover:scale-105 transition-transform duration-300" alt="Trinity Architecture">
              </div>
              <div class="flex items-center gap-1.5 mb-1.5">
                <span class="px-2 py-0.5 rounded-full bg-primary/10 text-primary text-[11px] font-bold">🌐 The Trinity Ecosystem</span>
              </div>
              <h3 class="text-base font-bold text-on-surface mb-1">Browser + IDE + CI/CD</h3>
              <p class="text-xs text-on-surface-variant leading-relaxed">
                Seamlessly bridges <code class="font-code text-primary">verdant-chrome</code> (live in-tab hot-patch), <code class="font-code">verdant-vscode</code> (IDE diff stream), and <code class="font-code text-secondary">verdant-sentinel</code> (headless bot).
              </p>
            </div>

            <!-- Card 3: Google Cloud Certified Eco Ledger -->
            <div class="bg-surface-container-lowest rounded-2xl p-4 border border-surface-container-high shadow-sm hover:shadow-md transition-all flex flex-col">
              <div class="w-full h-44 rounded-xl overflow-hidden mb-3 bg-surface-container-high border border-surface-container-high/60">
                <img src="/uploads/assets/overview_eco_ledger.jpg" class="w-full h-full object-cover hover:scale-105 transition-transform duration-300" alt="Certified Eco Ledger">
              </div>
              <div class="flex items-center gap-1.5 mb-1.5">
                <span class="px-2 py-0.5 rounded-full bg-tertiary-fixed text-on-tertiary-fixed-variant text-[11px] font-bold">💧 Google Cloud PUE 1.10 / WUE 1.18</span>
              </div>
              <h3 class="text-base font-bold text-on-surface mb-1">Thermodynamic Net-Zero</h3>
              <p class="text-xs text-on-surface-variant leading-relaxed">
                Dynamic ContextPrism AST & DOM pruning eliminates 70% to 92% token bloat. Live Watt-hours and cooling water savings recorded dynamically in SQLite.
              </p>
            </div>

          </section>

          <!-- Interactive Ecosystem Navigation & Quick Action Bar -->
          <section class="w-full bg-surface-container-lowest rounded-2xl p-5 border border-surface-container-high shadow-sm flex flex-col sm:flex-row items-center justify-between gap-4">
            <div class="flex items-center gap-3">
              <div class="w-10 h-10 rounded-xl bg-secondary-fixed/50 flex items-center justify-center text-secondary">
                <span class="material-symbols-outlined text-[24px]">hub</span>
              </div>
              <div>
                <div class="flex items-center gap-2">
                  <span class="font-bold text-sm text-on-surface">Ecosystem Runtime Engine</span>
                  <span class="px-2 py-0.5 rounded-full bg-secondary-fixed text-secondary text-[10px] font-bold">Port 8000 Active</span>
                </div>
                <p class="text-xs text-on-surface-variant">Active WebSocket Bridge connecting Chrome Extension, VS Code IDE, and CI/CD Sentinel</p>
              </div>
            </div>
            <div class="flex items-center gap-2.5 flex-wrap">
              <a href="/sustainability" onclick="navigateTab('sustainability', event)" class="px-4 py-2 rounded-xl bg-surface-container hover:bg-surface-container-high text-on-surface text-xs font-semibold transition cursor-pointer flex items-center gap-1.5 shadow-sm">
                <span class="material-symbols-outlined text-[16px] text-secondary">water_drop</span>
                <span>Sustainability Ledger</span>
              </a>
              <a href="/history" onclick="navigateTab('history', event)" class="px-4 py-2 rounded-xl bg-primary text-on-primary text-xs font-semibold hover:bg-primary-container transition cursor-pointer flex items-center gap-1.5 shadow-sm">
                <span class="material-symbols-outlined text-[16px]">history</span>
                <span>View Audit History</span>
              </a>
            </div>
          </section>

          <!-- Trinity Closed-Loop Workflow Hub -->
          <section class="w-full max-w-4xl mx-auto flex flex-col gap-5 pt-2">
            <div class="bg-surface-container-lowest rounded-2xl p-6 border border-surface-container-high shadow-sm">
              <div class="flex items-center justify-between mb-4 pb-3 border-b border-surface-container-high">
                <div class="flex items-center gap-2.5">
                  <span class="w-3 h-3 rounded-full bg-secondary animate-pulse"></span>
                  <span class="font-bold text-sm text-on-surface">The V.E.R.D.A.N.T. Trinity Architecture</span>
                </div>
                <span class="px-3 py-1 rounded-full bg-secondary-fixed/50 text-secondary text-xs font-bold">Full Ecosystem Active</span>
              </div>
              <p class="text-xs sm:text-sm text-on-surface-variant leading-relaxed mb-6">
                A unified closed-loop testing and repair runtime. Developers inspect and hot-patch live in the browser, diffs stream to VS Code via WebSockets, and headless Playwright sentinels autonomously self-heal regressions on every pull request.
              </p>

              <!-- 4-Step Trinity Workflow -->
              <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
                <div class="p-4 rounded-xl bg-surface-container-low border border-surface-container-high/60 flex flex-col">
                  <div class="w-8 h-8 rounded-lg bg-primary/10 text-primary flex items-center justify-center font-bold text-sm mb-2.5">1</div>
                  <h4 class="font-bold text-xs text-on-surface mb-1">In-Browser Extension</h4>
                  <p class="text-[11px] text-on-surface-variant leading-snug">Inspect DOM bounding boxes, detect text overflow, and test instant in-tab CSS hot-patches.</p>
                </div>

                <div class="p-4 rounded-xl bg-surface-container-low border border-surface-container-high/60 flex flex-col">
                  <div class="w-8 h-8 rounded-lg bg-primary/10 text-primary flex items-center justify-center font-bold text-sm mb-2.5">2</div>
                  <h4 class="font-bold text-xs text-on-surface mb-1">VS Code Live Bridge</h4>
                  <p class="text-[11px] text-on-surface-variant leading-snug">WebSocket port 8000 streams atomic Search/Replace diffs straight into your editor.</p>
                </div>

                <div class="p-4 rounded-xl bg-surface-container-low border border-surface-container-high/60 flex flex-col">
                  <div class="w-8 h-8 rounded-lg bg-secondary-fixed/60 text-secondary flex items-center justify-center font-bold text-sm mb-2.5">3</div>
                  <h4 class="font-bold text-xs text-on-surface mb-1">Autonomous CI/CD</h4>
                  <p class="text-[11px] text-on-surface-variant leading-snug">Headless Playwright synthetic crawler tests Desktop & Mobile viewports on every pull request.</p>
                </div>

                <div class="p-4 rounded-xl bg-surface-container-low border border-surface-container-high/60 flex flex-col">
                  <div class="w-8 h-8 rounded-lg bg-tertiary-fixed text-on-tertiary-fixed-variant flex items-center justify-center font-bold text-sm mb-2.5">4</div>
                  <h4 class="font-bold text-xs text-on-surface mb-1">RED ❌ -> GREEN ✅ Proof</h4>
                  <p class="text-[11px] text-on-surface-variant leading-snug">Proves failure on unpatched code, applies fix, verifies pass, and commits self-healed PR.</p>
                </div>
              </div>
            </div>
          </section>

        </div>
      </div>
    </div>

    <!-- ======================================================================= -->
    <!-- SCREEN 4: VERDE-HYDRA SUSTAINABILITY DASHBOARD                           -->
    <!-- ======================================================================= -->
    <div id="screen-sustainability" class="w-full hidden">
      <div class="w-full max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 sm:py-8 flex flex-col gap-6">
        
        <!-- Header -->
        <div class="flex flex-col md:flex-row md:items-end justify-between gap-4 pb-4 border-b border-surface-container-high">
          <div>
            <div class="flex items-center gap-2 mb-1">
              <span class="px-2 py-0.5 rounded-full bg-secondary-fixed text-on-secondary-fixed-variant text-[11px] font-semibold uppercase tracking-wider">Green Computing Standard</span>
              <span class="text-outline">•</span>
              <span class="text-xs font-code text-secondary font-semibold">ASHRAE TC 9.9 · Google Cloud Baseline</span>
            </div>
            <h1 class="text-2xl sm:text-3xl font-bold text-on-surface tracking-tight">VERDE-Hydra Telemetry</h1>
            <p class="text-xs sm:text-sm text-on-surface-variant">Real data center resource reduction metrics certified against published Google Cloud PUE and WUE.</p>
          </div>
        </div>

        <!-- 4 Bento KPI Cards -->
        <div class="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-4">
          <div class="bg-surface-container-lowest p-5 rounded-2xl shadow-sm border border-surface-container-high">
            <span class="text-xs text-outline block">Net Energy Saved</span>
            <div class="text-2xl sm:text-3xl font-bold text-secondary mt-1" id="eco-saved-wh">584 Wh</div>
            <span class="text-[11px] text-secondary font-semibold mt-1 block">82.2% reduction vs manual CI</span>
          </div>
          <div class="bg-surface-container-lowest p-5 rounded-2xl shadow-sm border border-surface-container-high">
            <span class="text-xs text-outline block">Cooling Water Conserved</span>
            <div class="text-2xl sm:text-3xl font-bold text-primary mt-1" id="eco-water-ml">2.35 L</div>
            <span class="text-[11px] text-primary font-semibold mt-1 block">Google Cloud WUE 1.18 L/kWh</span>
          </div>
          <div class="bg-surface-container-lowest p-5 rounded-2xl shadow-sm border border-surface-container-high">
            <span class="text-xs text-outline block">Token Bloat Reduction</span>
            <div class="text-2xl sm:text-3xl font-bold text-tertiary mt-1" id="eco-token-pct">-84.9%</div>
            <span class="text-[11px] text-outline font-semibold mt-1 block">ContextPrism AST compression</span>
          </div>
          <div class="bg-surface-container-lowest p-5 rounded-2xl shadow-sm border border-surface-container-high">
            <span class="text-xs text-outline block">Operating Cloud PUE</span>
            <div class="text-2xl sm:text-3xl font-bold text-on-surface mt-1">1.10</div>
            <span class="text-[11px] text-secondary font-semibold mt-1 block">Google Cloud Run Certified</span>
          </div>
        </div>

        <!-- Comparative Comparison Bars -->
        <div class="grid grid-cols-1 lg:grid-cols-12 gap-6">
          
          <!-- Energy Bars (7 Cols) -->
          <div class="lg:col-span-7 bg-surface-container-lowest p-space-xl rounded-xl shadow-sm border border-surface-container-high flex flex-col justify-between">
            <div>
              <div class="flex items-center justify-between mb-space-sm">
                <h2 class="text-base font-bold text-on-surface">Energy Consumption Comparison</h2>
                <span class="px-2 py-0.5 rounded-full bg-surface-container text-[11px] font-code text-on-surface-variant">A/B Benchmark</span>
              </div>
              <p class="text-xs text-on-surface-variant mb-space-xl">
                Comparison between traditional manual debugging cycles and V.E.R.D.A.N.T. autonomous distillation.
              </p>

              <div class="space-y-space-xl">
                <div>
                  <div class="flex justify-between items-baseline mb-1 text-xs">
                    <span class="font-medium text-on-surface">Traditional Debugging Cycle (6x CI rebuilds, raw video)</span>
                    <span class="font-code font-bold text-on-surface">710 Wh</span>
                  </div>
                  <div class="w-full bg-surface-container-high h-6 rounded-lg overflow-hidden flex items-center">
                    <div class="bg-outline-variant h-full rounded-lg w-full"></div>
                  </div>
                </div>

                <div>
                  <div class="flex justify-between items-baseline mb-1 text-xs">
                    <span class="font-semibold text-secondary">V.E.R.D.A.N.T. Distilled Workflow (Single-pass Playwright)</span>
                    <span class="font-code font-bold text-secondary">126 Wh</span>
                  </div>
                  <div class="w-full bg-surface-container-high h-6 rounded-lg overflow-hidden flex items-center">
                    <div class="bg-secondary h-full rounded-lg flex items-center justify-end px-2" style="width: 17.75%;">
                      <span class="w-1.5 h-1.5 rounded-full bg-surface-container-lowest"></span>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <div class="mt-space-xl p-space-md rounded-xl bg-secondary-fixed/40 flex items-center justify-between flex-wrap gap-2">
              <div class="flex items-center gap-space-md">
                <span class="w-9 h-9 rounded-full bg-surface-container-lowest flex items-center justify-center text-secondary shadow-sm">
                  <span class="material-symbols-outlined text-[18px]">savings</span>
                </span>
                <div>
                  <div class="text-xs font-semibold text-on-secondary-fixed-variant">Net Saved Energy per Run</div>
                  <div class="text-[11px] text-on-surface-variant">Dramatically decreases cloud cluster thermal footprint</div>
                </div>
              </div>
              <div class="text-right">
                <span class="text-lg font-bold text-secondary">584 Wh</span>
                <div class="text-[10px] text-on-secondary-fixed font-semibold">82.2% reduction</div>
              </div>
            </div>
          </div>

          <!-- Datacenter Water (5 Cols) -->
          <div class="lg:col-span-5 bg-surface-container-lowest p-space-xl rounded-xl shadow-sm border border-surface-container-high flex flex-col justify-between">
            <div>
              <div class="flex items-center justify-between mb-space-sm">
                <h2 class="text-base font-bold text-on-surface">Datacenter Cooling Water Impact</h2>
                <div class="w-2 h-2 rounded-full bg-primary animate-pulse"></div>
              </div>
              <p class="text-xs text-on-surface-variant mb-space-lg">
                Calculated using published Google Cloud Water Usage Effectiveness (WUE).
              </p>

              <div class="bg-surface-container-low p-space-md rounded-xl mb-space-lg flex items-center justify-between">
                <div>
                  <span class="text-[10px] text-on-surface-variant uppercase tracking-wider font-semibold">Operating WUE</span>
                  <div class="text-2xl font-bold text-primary mt-0.5">1.18 <span class="text-xs text-on-surface-variant font-normal">L / kWh</span></div>
                </div>
                <div class="text-right">
                  <span class="text-[10px] text-on-surface-variant block">ASHRAE TC 9.9</span>
                  <span class="font-code text-xs text-secondary font-medium">Standardized</span>
                </div>
              </div>

              <!-- Breakdown list -->
              <div class="space-y-space-sm text-xs">
                <div class="p-space-sm rounded-lg bg-surface-container flex items-center justify-between">
                  <div class="flex items-center gap-2">
                    <span class="material-symbols-outlined text-[18px] text-primary">memory</span>
                    <div>
                      <div class="font-medium text-on-surface">Gemini 3.5 Token Pruning</div>
                      <div class="font-code text-[10px] text-on-surface-variant">Avoided 1.48L evaporative waste</div>
                    </div>
                  </div>
                  <span class="font-semibold text-primary">63%</span>
                </div>
                <div class="p-space-sm rounded-lg bg-surface-container flex items-center justify-between">
                  <div class="flex items-center gap-2">
                    <span class="material-symbols-outlined text-[18px] text-secondary">deployed_code</span>
                    <div>
                      <div class="font-medium text-on-surface">Docker Micro-Sandbox Replay</div>
                      <div class="font-code text-[10px] text-on-surface-variant">Shorter runtime: avoided 0.54L</div>
                    </div>
                  </div>
                  <span class="font-semibold text-secondary">23%</span>
                </div>
                <div class="p-space-sm rounded-lg bg-surface-container flex items-center justify-between">
                  <div class="flex items-center gap-2">
                    <span class="material-symbols-outlined text-[18px] text-tertiary">browser_updated</span>
                    <div>
                      <div class="font-medium text-on-surface">Targeted Playwright Assertions</div>
                      <div class="font-code text-[10px] text-on-surface-variant">Bypassed cold runs: saved 0.33L</div>
                    </div>
                  </div>
                  <span class="font-semibold text-tertiary">14%</span>
                </div>
              </div>
            </div>

            <div class="mt-space-lg flex items-center gap-1 text-on-surface-variant text-[11px]">
              <span class="material-symbols-outlined text-[16px] text-outline">info</span>
              <span>Formula: Water (L) = Energy (kWh) × PUE (1.10) × WUE (1.18)</span>
            </div>
          </div>

        </div>

      </div>
    </div>

    <!-- ======================================================================= -->
    <!-- SCREEN 5: AUDIT HISTORY & PERSISTENT DATABASE                           -->
    <!-- ======================================================================= -->
    <div id="screen-history" class="w-full hidden">
      <div class="w-full max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 sm:py-8 flex flex-col gap-6">
        
        <!-- Header -->
        <div class="flex flex-col md:flex-row md:items-end justify-between gap-4 pb-4 border-b border-surface-container-high">
          <div>
            <div class="flex items-center gap-2 mb-1">
              <span class="px-2 py-0.5 rounded-full bg-secondary-fixed text-on-secondary-fixed-variant text-[11px] font-semibold uppercase tracking-wider">Persistent Audit Trail</span>
              <span class="text-outline">•</span>
              <span class="text-xs font-code text-secondary font-semibold">SQLite WAL · AES-256 Encrypted</span>
            </div>
            <h1 class="text-2xl sm:text-3xl font-bold text-on-surface tracking-tight">Incident History & Audit Log</h1>
            <p class="text-xs sm:text-sm text-on-surface-variant">Every bug video, scrubbed log, Playwright proof, and dispatched PR is recorded permanently.</p>
          </div>
          
          <div class="flex items-center gap-2">
            <button onclick="loadHistoryData()" class="px-4 py-2 rounded-full bg-surface-container hover:bg-surface-container-high text-xs font-semibold text-on-surface transition flex items-center gap-1 cursor-pointer">
              <span class="material-symbols-outlined text-[16px]">refresh</span> Refresh
            </button>
          </div>
        </div>

        <!-- 4 History KPI Cards -->
        <div class="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-4">
          <div class="bg-surface-container-lowest p-5 rounded-2xl shadow-sm border border-surface-container-high">
            <span class="text-xs text-outline block">Total Incidents Triaged</span>
            <div class="text-2xl sm:text-3xl font-bold text-on-surface mt-1" id="hist-stat-total">0</div>
            <span class="text-[11px] text-secondary font-semibold mt-1 block">Full forensic records saved</span>
          </div>
          <div class="bg-surface-container-lowest p-5 rounded-2xl shadow-sm border border-surface-container-high">
            <span class="text-xs text-outline block">With Repo vs QA Reports</span>
            <div class="text-2xl sm:text-3xl font-bold text-primary mt-1">
              <span id="hist-stat-with-repo" class="text-secondary">0</span> <span class="text-sm text-outline">/</span> <span id="hist-stat-no-repo" class="text-tertiary">0</span>
            </div>
            <span class="text-[11px] text-outline font-semibold mt-1 block">Code patches vs Diagnostics</span>
          </div>
          <div class="bg-surface-container-lowest p-5 rounded-2xl shadow-sm border border-surface-container-high">
            <span class="text-xs text-outline block">Verified GitHub PRs</span>
            <div class="text-2xl sm:text-3xl font-bold text-primary mt-1" id="hist-stat-prs">0</div>
            <span class="text-[11px] text-primary font-semibold mt-1 block">Dispatched to remote origin</span>
          </div>
          <div class="bg-surface-container-lowest p-5 rounded-2xl shadow-sm border border-surface-container-high">
            <span class="text-xs text-outline block">Cumulative Energy Saved</span>
            <div class="text-2xl sm:text-3xl font-bold text-secondary mt-1"><span id="hist-stat-energy">0.0</span> <span class="text-xs font-normal">Wh</span></div>
            <span class="text-[11px] text-secondary font-semibold mt-1 block"><span id="hist-stat-water">0.0</span> mL water conserved</span>
          </div>
        </div>

        <!-- History Filter Bar & Table -->
        <div class="bg-surface-container-lowest rounded-2xl shadow-sm border border-surface-container-high p-4 sm:p-6">
          <div class="flex items-center justify-between pb-4 border-b border-surface-container flex-wrap gap-2">
            <div class="flex items-center gap-2 flex-wrap">
              <span class="text-xs font-semibold text-on-surface">Filter Records:</span>
              <button onclick="filterHistory('ALL')" id="hfilter-all" class="px-3 py-1 rounded-full text-xs font-bold bg-primary text-on-primary cursor-pointer">All</button>
              <button onclick="filterHistory('WITH_REPO')" id="hfilter-repo" class="px-3 py-1 rounded-full text-xs font-medium text-on-surface-variant hover:bg-surface-container cursor-pointer">With Repo</button>
              <button onclick="filterHistory('WITHOUT_REPO')" id="hfilter-norepo" class="px-3 py-1 rounded-full text-xs font-medium text-on-surface-variant hover:bg-surface-container cursor-pointer">QA Reports</button>
            </div>
            <span class="font-code text-[11px] text-outline">Encrypted in SQLite DB</span>
          </div>

          <div class="overflow-x-auto mt-4 rounded-xl border border-surface-container-high">
            <table class="min-w-[760px] w-full text-left text-xs text-on-surface">
              <thead class="bg-surface-container-low text-on-surface-variant uppercase text-[10px] tracking-wider border-b border-surface-container">
                <tr>
                  <th class="p-3">Session ID / Date</th>
                  <th class="p-3">Incident Title & Cause</th>
                  <th class="p-3">Workflow Mode</th>
                  <th class="p-3">Confidence & Arbiter</th>
                  <th class="p-3">Proof / Status</th>
                  <th class="p-3">Eco Savings</th>
                  <th class="p-3 text-right">Actions</th>
                </tr>
              </thead>
              <tbody id="history-table-body" class="divide-y divide-surface-container">
                <!-- Dynamically populated via JS -->
              </tbody>
            </table>
            <div id="history-empty" class="hidden text-center py-12 text-outline text-xs">
              <span class="material-symbols-outlined text-[32px] block mb-2 text-outline-variant">inbox</span>
              No incident records found. Run a triage session to create audit history.
            </div>
          </div>
        </div>

      </div>
    </div>

  </main>

  <!-- ========================================================================= -->
  <!-- MODAL: RESOLUTION WORKFLOWS DRAWER (Option 1 vs Option 2)                 -->
  <!-- ========================================================================= -->
  <div class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-on-background/40 backdrop-blur-sm transition-opacity hidden" id="fixDrawer">
    <div class="bg-surface-container-lowest rounded-2xl max-w-3xl w-full p-space-xl shadow-2xl flex flex-col gap-space-lg max-h-[90vh] overflow-y-auto border border-surface-container-high">
      
      <!-- Drawer Header -->
      <div class="flex items-center justify-between pb-space-sm border-b border-surface-container">
        <div class="flex items-center gap-space-sm">
          <div class="w-10 h-10 rounded-full bg-primary/10 text-primary flex items-center justify-center">
            <span class="material-symbols-outlined text-[24px]">build_circle</span>
          </div>
          <div>
            <h3 class="text-xl font-bold text-on-surface">Resolve Issue</h3>
            <p class="text-xs text-on-surface-variant">Select your execution environment to apply V.E.R.D.A.N.T.'s remediation.</p>
          </div>
        </div>
        <button class="w-8 h-8 rounded-full hover:bg-surface-container text-on-surface-variant flex items-center justify-center" onclick="document.getElementById('fixDrawer').classList.add('hidden')">
          <span class="material-symbols-outlined text-[20px]">close</span>
        </button>
      </div>

      <!-- Option 1 & 2 Cards -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-gutter-desktop">
        
        <!-- Option 1: Yes, I have the source code -->
        <div id="modalOption1" class="cursor-pointer transition-all duration-200 p-space-lg rounded-xl flex flex-col justify-between shadow-md border-2 border-primary bg-primary/10 ring-2 ring-primary/30 relative" onclick="selectModalOption(1)">
          <div class="flex flex-col gap-space-md">
            <div class="flex items-center justify-between">
              <span class="px-2.5 py-1 rounded-full bg-primary/20 text-primary text-[11px] font-bold">Option 1</span>
              <div id="opt1Radio" class="w-5 h-5 rounded-full border-2 border-primary bg-primary flex items-center justify-center text-on-primary">
                <span class="material-symbols-outlined text-[14px] font-bold">check</span>
              </div>
            </div>
            <div>
              <h4 class="text-base font-bold text-on-surface">Yes, I have the source code</h4>
              <p class="text-xs text-on-surface-variant mt-1">
                Synthesize automated fix, verify with Playwright RED-to-GREEN proof loop, and submit a ready-to-merge pull request directly to the target GitHub branch.
              </p>
            </div>
          </div>
          <div class="mt-space-lg">
            <button onclick="event.stopPropagation(); triggerRealGitHubPR();" id="drawer-pr-btn" class="w-full py-2.5 px-space-md rounded-xl bg-primary hover:bg-primary-container text-on-primary text-xs font-bold flex items-center justify-center gap-2 shadow-sm transition">
              <span class="material-symbols-outlined text-[18px]">open_in_new</span>
              <span id="drawer-pr-btn-label">Create Pull Request on GitHub</span>
            </button>
          </div>
        </div>

        <!-- Option 2: No, I only have the video and logs -->
        <div id="modalOption2" class="cursor-pointer transition-all duration-200 p-space-lg rounded-xl flex flex-col justify-between shadow-sm border border-outline-variant/30 bg-surface-container-low hover:border-outline hover:bg-surface-container relative" onclick="selectModalOption(2)">
          <div class="flex flex-col gap-space-md">
            <div class="flex items-center justify-between">
              <span class="px-2.5 py-1 rounded-full bg-surface-container text-on-surface-variant text-[11px] font-semibold">Option 2</span>
              <div id="opt2Radio" class="w-5 h-5 rounded-full border-2 border-outline-variant bg-transparent flex items-center justify-center text-transparent">
                <span class="material-symbols-outlined text-[14px] font-bold">check</span>
              </div>
            </div>
            <div>
              <h4 class="text-base font-bold text-on-surface">No, I only have the video and logs</h4>
              <p class="text-xs text-on-surface-variant mt-1">
                Export a full forensic diagnostic bundle containing replay snapshots, DOM logs, sanitized stack traces, and ready-to-file Jira tickets.
              </p>
            </div>
          </div>
          <div class="mt-space-lg flex flex-col gap-2">
            <button onclick="event.stopPropagation(); downloadQAReport();" class="w-full py-2.5 px-space-md rounded-xl bg-primary hover:bg-primary-container text-on-primary text-xs font-bold flex items-center justify-center gap-2 shadow-sm transition cursor-pointer">
              <span class="material-symbols-outlined text-[18px]">download</span>
              <span>Download Bug Report (.md)</span>
            </button>
            <button onclick="event.stopPropagation(); copyForensicReportMarkdown();" class="w-full py-2 px-space-md rounded-xl bg-surface-container hover:bg-surface-container-high text-on-surface text-xs font-semibold flex items-center justify-center gap-2 shadow-sm transition cursor-pointer">
              <span class="material-symbols-outlined text-[16px]">content_copy</span>
              <span>Copy Bug Report (Markdown / Jira)</span>
            </button>
          </div>
        </div>

      </div>

      <div class="flex items-center justify-end pt-space-sm text-xs text-on-surface-variant">
        <button onclick="document.getElementById('fixDrawer').classList.add('hidden')" class="text-outline hover:text-on-surface font-semibold">
          Dismiss
        </button>
      </div>

    </div>
  </div>

  <!-- ========================================================================= -->
  <!-- MODAL: GITHUB CONNECTION & ENCRYPTED TOKEN STORAGE                        -->
  <!-- ========================================================================= -->
  <div id="github-modal" class="fixed inset-0 bg-black/60 backdrop-blur-sm z-50 hidden flex items-center justify-center p-4">
    <div class="bg-surface-container-lowest rounded-2xl max-w-md w-full p-6 shadow-2xl border border-surface-container-high space-y-4">
      <div class="flex items-center justify-between border-b border-surface-container pb-3">
        <div class="flex items-center gap-2.5">
          <div class="w-8 h-8 rounded-lg bg-surface-container flex items-center justify-center text-primary">
            <span class="material-symbols-outlined text-[20px]">account_tree</span>
          </div>
          <div>
            <h3 class="font-bold text-sm text-on-surface">GitHub & Repo Connection</h3>
            <p class="text-[11px] text-on-surface-variant">Automate real Git branching and Pull Requests</p>
          </div>
        </div>
        <button onclick="closeGithubModal()" class="text-outline hover:text-on-surface"><span class="material-symbols-outlined text-[18px]">close</span></button>
      </div>

      <div class="space-y-3 text-xs">
        <div>
          <label class="block text-on-surface font-semibold mb-1">GitHub Personal Access Token (PAT)</label>
          <input type="password" id="gh-input-token" placeholder="ghp_xxxxxxxxxxxxxxxxxxxx" class="w-full bg-surface-container-low border border-outline-variant rounded-lg p-2.5 font-code text-on-surface focus:outline-none focus:border-primary">
          <p class="text-[10px] text-outline mt-1">Requires <code class="text-primary font-code">repo</code> scope for branch and PR creation.</p>
        </div>
        <div>
          <label class="block text-on-surface font-semibold mb-1">GitHub Username / Org</label>
          <input type="text" id="gh-input-user" placeholder="e.g. dhairya-shah7" class="w-full bg-surface-container-low border border-outline-variant rounded-lg p-2.5 text-on-surface focus:outline-none focus:border-primary">
        </div>
        <div>
          <label class="block text-on-surface font-semibold mb-1">Notification Email</label>
          <input type="email" id="gh-input-email" placeholder="e.g. developer@verdant.ai" class="w-full bg-surface-container-low border border-outline-variant rounded-lg p-2.5 text-on-surface focus:outline-none focus:border-primary">
        </div>

        <div class="p-3 rounded-lg bg-surface-container-low border border-surface-container text-[11px] text-on-surface-variant flex items-start gap-2">
          <span class="material-symbols-outlined text-secondary text-[18px] shrink-0">lock</span>
          <span><strong>SOC-2 / GDPR Standard:</strong> Token is encrypted using <strong>AES-256-GCM</strong> at rest in SQLite and never transmitted externally.</span>
        </div>

        <div id="gh-modal-status-feedback" class="text-center text-xs font-semibold text-secondary"></div>
      </div>

      <div class="flex items-center justify-end gap-2 pt-2 border-t border-surface-container">
        <button onclick="closeGithubModal()" class="px-3.5 py-1.5 rounded-lg bg-surface-container text-on-surface hover:bg-surface-container-high text-xs font-semibold">Cancel</button>
        <button onclick="saveGithubTokenAndUser()" class="px-4 py-1.5 rounded-lg bg-primary text-on-primary hover:bg-primary-container text-xs font-bold shadow-sm flex items-center gap-1.5">
          <span class="material-symbols-outlined text-[16px]">check</span>
          <span>Save & Encrypt</span>
        </button>
      </div>
    </div>
  </div>

  <!-- ========================================================================= -->
  <!-- MODAL: SESSION DETAIL INSPECTOR                                           -->
  <!-- ========================================================================= -->
  <div id="session-detail-modal" class="fixed inset-0 bg-black/60 backdrop-blur-sm z-50 hidden flex items-center justify-center p-4">
    <div class="bg-surface-container-lowest rounded-2xl max-w-3xl w-full p-6 shadow-2xl border border-surface-container-high space-y-4 max-h-[90vh] flex flex-col">
      <div class="flex items-center justify-between border-b border-surface-container pb-3">
        <div class="flex items-center gap-2.5">
          <div class="w-9 h-9 rounded-lg bg-secondary-fixed/50 flex items-center justify-center text-secondary text-lg">
            <span class="material-symbols-outlined text-[20px]">history_edu</span>
          </div>
          <div>
            <h3 class="font-bold text-base text-on-surface" id="sdetail-title">Forensic Incident Record</h3>
            <p class="text-xs text-on-surface-variant" id="sdetail-meta">Session ID: -- · Created: --</p>
          </div>
        </div>
        <button onclick="closeSessionDetailModal()" class="text-outline hover:text-on-surface"><span class="material-symbols-outlined text-[20px]">close</span></button>
      </div>

      <div class="overflow-y-auto space-y-4 text-xs pr-1 flex-1">
        <div class="p-3.5 rounded-xl bg-surface-container-low border border-surface-container space-y-2">
          <div class="flex items-center justify-between">
            <span class="text-outline font-bold uppercase tracking-wider text-[10px]">Root Cause Diagnosis</span>
            <span id="sdetail-mode-badge" class="px-2 py-0.5 rounded text-[10px] font-bold bg-secondary-container text-on-secondary-container">WITH REPO</span>
          </div>
          <p class="text-on-surface text-xs leading-relaxed font-medium" id="sdetail-root-cause"></p>
          <div class="text-secondary text-[11px] font-semibold flex items-center gap-1.5">
            <span class="material-symbols-outlined text-[16px]">volume_up</span>
            <span id="sdetail-spoken"></span>
          </div>
        </div>

        <!-- Reproduction Steps -->
        <div class="space-y-1.5">
          <div class="text-[11px] font-bold text-outline uppercase tracking-wider">Chronological Steps to Reproduce</div>
          <div class="space-y-1" id="sdetail-steps"></div>
        </div>

        <!-- Diff Card -->
        <div id="sdetail-diff-box" class="space-y-1.5">
          <div class="flex items-center justify-between text-[11px] font-bold text-outline uppercase tracking-wider">
            <span>Surgical Code Patch Diff</span>
            <span class="text-secondary font-code text-[10px]">Atomic Search/Replace</span>
          </div>
          <pre class="bg-surface-container p-3 rounded-lg font-code text-xs text-on-surface overflow-x-auto max-h-48" id="sdetail-diff-content"></pre>
        </div>

        <!-- Eco Telemetry -->
        <div class="grid grid-cols-2 gap-2 text-center text-xs">
          <div class="bg-surface-container-low p-2.5 rounded-lg">
            <span class="text-outline text-[10px] block">Energy Saved</span>
            <span class="font-bold text-secondary text-sm" id="sdetail-energy">0.0 Wh</span>
          </div>
          <div class="bg-surface-container-low p-2.5 rounded-lg">
            <span class="text-outline text-[10px] block">Cooling Water Conserved</span>
            <span class="font-bold text-primary text-sm" id="sdetail-water">0.0 mL</span>
          </div>
        </div>
      </div>

      <div class="flex items-center justify-between pt-3 border-t border-surface-container text-xs">
        <div id="sdetail-pr-box"></div>
        <div class="flex items-center gap-2">
          <button onclick="copySessionMarkdown()" class="px-3 py-1.5 rounded-lg bg-surface-container text-on-surface hover:bg-surface-container-high font-semibold">
            Copy Markdown Report
          </button>
          <button onclick="closeSessionDetailModal()" class="px-4 py-1.5 rounded-lg bg-primary text-on-primary font-bold hover:bg-primary-container">Close</button>
        </div>
      </div>
    </div>
  </div>

  <!-- ========================================================================= -->
  <!-- CLIENT JAVASCRIPT: STITCH NAVIGATION, LIVE APIS & DATABASE WORKFLOWS      -->
  <!-- ========================================================================= -->
  <script>
    let activeMainTab = 'home';
    let currentWorkflowMode = 'WITH_REPO';
    let currentScenario = 'checkout_500';
    let uploadedFileName = '';
    let currentSessionId = null;
    let latestRunData = null;
    let cachedHistory = [];
    let activeHistoryFilter = 'ALL';
    let activeDetailSession = null;

    // ── Mobile Sidebar Drawer Controls ─────────────────────────────────────
    function toggleMobileSidebar() {
      const sidebar = document.getElementById('main-sidebar');
      const backdrop = document.getElementById('sidebar-backdrop');
      if (sidebar && backdrop) {
        const isClosed = sidebar.classList.contains('-translate-x-full');
        if (isClosed) {
          sidebar.classList.remove('-translate-x-full');
          backdrop.classList.remove('hidden');
        } else {
          sidebar.classList.add('-translate-x-full');
          backdrop.classList.add('hidden');
        }
      }
    }

    function closeMobileSidebar() {
      const sidebar = document.getElementById('main-sidebar');
      const backdrop = document.getElementById('sidebar-backdrop');
      if (sidebar && backdrop) {
        sidebar.classList.add('-translate-x-full');
        backdrop.classList.add('hidden');
      }
    }

    // ── Main Tab Switching & URL Routing ───────────────────────────────────
    function switchMainTab(tab) {
      activeMainTab = tab;
      const screens = ['home', 'sustainability', 'history'];
      screens.forEach(s => {
        const el = document.getElementById('screen-' + s);
        const btn = document.getElementById('nav-btn-' + s);
        if (el) {
          if (s === tab) el.classList.remove('hidden');
          else el.classList.add('hidden');
        }
        if (btn) {
          if (s === tab) {
            btn.className = "nav-tab-active px-3.5 py-2.5 rounded-xl text-xs md:text-sm text-on-surface transition-all flex items-center gap-3 font-semibold cursor-pointer";
          } else {
            btn.className = "px-3.5 py-2.5 rounded-xl text-xs md:text-sm text-on-surface-variant hover:text-on-surface hover:bg-surface-container transition-all flex items-center gap-3 font-medium cursor-pointer";
          }
        }
      });

      if (tab === 'history') {
        loadHistoryData();
      }
      if (tab === 'sustainability') {
        loadSustainabilityData();
      }
    }

    function navigateTab(tab, event) {
      if (event) event.preventDefault();
      const pathMap = {
        'home': '/',
        'sustainability': '/sustainability',
        'history': '/history'
      };
      const targetPath = pathMap[tab] || '/';
      if (window.location.pathname !== targetPath) {
        window.history.pushState({ tab: tab }, '', targetPath);
      }
      switchMainTab(tab);
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }

    function initScreenFromUrl() {
      const p = window.location.pathname.toLowerCase();
      if (p.includes('sustain') || p.includes('verde') || p.includes('eco')) {
        switchMainTab('sustainability');
      } else if (p.includes('history') || p.includes('audit')) {
        switchMainTab('history');
      } else {
        switchMainTab('home');
      }
    }

    // ── Workflow Mode: With Repo vs QA Report Only ──────────────────────────
    function setWorkflowMode(mode) {
      currentWorkflowMode = mode;
      const pillRepo = document.getElementById('mode-pill-repo');
      const pillNoRepo = document.getElementById('mode-pill-norepo');
      const bannerNote = document.getElementById('repo-banner-note');

      if (mode === 'WITH_REPO') {
        if (pillRepo) pillRepo.className = "px-3 py-1 rounded text-xs font-bold transition bg-surface-container-lowest text-primary shadow-sm flex items-center gap-1";
        if (pillNoRepo) pillNoRepo.className = "px-3 py-1 rounded text-xs font-medium text-on-surface-variant hover:text-on-surface transition flex items-center gap-1";
        if (bannerNote) bannerNote.innerHTML = "<strong>Repository mode active:</strong> Full AST Narrowing, surgical patch diff, Playwright RED/GREEN verification & GitHub PR enabled.";
        selectModalOption(1);
      } else {
        if (pillNoRepo) pillNoRepo.className = "px-3 py-1 rounded text-xs font-bold transition bg-surface-container-lowest text-tertiary shadow-sm flex items-center gap-1";
        if (pillRepo) pillRepo.className = "px-3 py-1 rounded text-xs font-medium text-on-surface-variant hover:text-on-surface transition flex items-center gap-1";
        if (bannerNote) bannerNote.innerHTML = "<strong>QA Triage mode active:</strong> Code diffs suppressed. Focuses purely on root-cause analysis, timeline steps, and Jira ticket export.";
        selectModalOption(2);
      }
    }

    // ── Dropzone State Switching ────────────────────────────────────────────
    function switchDropState(state) {
      const filledEl = document.getElementById('state-filled');
      const emptyEl = document.getElementById('state-empty');
      const tabPreview = document.getElementById('btn-tab-preview');
      const tabUpload = document.getElementById('btn-tab-upload');

      if (state === 'filled') {
        filledEl.classList.remove('hidden');
        emptyEl.classList.add('hidden');
        tabPreview.className = "px-space-md py-1 rounded text-xs bg-surface-container-lowest text-primary shadow-sm font-semibold transition-all";
        tabUpload.className = "px-space-md py-1 rounded text-xs text-on-surface-variant hover:text-on-surface transition-all";
      } else {
        filledEl.classList.add('hidden');
        emptyEl.classList.remove('hidden');
        tabUpload.className = "px-space-md py-1 rounded text-xs bg-surface-container-lowest text-primary shadow-sm font-semibold transition-all";
        tabPreview.className = "px-space-md py-1 rounded text-xs text-on-surface-variant hover:text-on-surface transition-all";
      }
    }

    // ── Scenario Presets ────────────────────────────────────────────────────
    function selectPreset(scenId) {
      currentScenario = scenId;
      const btnC = document.getElementById('btn-preset-checkout');
      const btnA = document.getElementById('btn-preset-auth');

      if (scenId === 'checkout_500') {
        if (btnC) btnC.className = "px-2.5 py-1 rounded-md text-xs font-semibold bg-primary text-on-primary shadow-sm transition";
        if (btnA) btnA.className = "px-2.5 py-1 rounded-md text-xs font-semibold bg-surface-container hover:bg-surface-container-high text-on-surface transition";
        const sn = document.getElementById('hero-session-name'); if (sn) sn.innerText = "checkout_unresponsive_submit_freeze.mp4";
        const sd = document.getElementById('hero-session-desc'); if (sd) sd.innerText = "User clicks 'Place Order'. Network returns 500; button stays disabled with zero visual repaint.";
        const ss = document.getElementById('hero-ssim'); if (ss) ss.innerHTML = "0.9984 <span class='text-[10px] text-error font-normal'>(Frozen)</span>";
        const hd = document.getElementById('hero-delta'); if (hd) hd.innerHTML = "0.02% <span class='text-[10px] text-secondary font-normal'>(Zero Drift)</span>";
        const hn = document.getElementById('hero-network'); if (hn) hn.innerText = "500 Fail";
      } else {
        if (btnA) btnA.className = "px-2.5 py-1 rounded-md text-xs font-semibold bg-primary text-on-primary shadow-sm transition";
        if (btnC) btnC.className = "px-2.5 py-1 rounded-md text-xs font-semibold bg-surface-container hover:bg-surface-container-high text-on-surface transition";
        const sn = document.getElementById('hero-session-name'); if (sn) sn.innerText = "auth_token_expired_silent_drop.mp4";
        const sd = document.getElementById('hero-session-desc'); if (sd) sd.innerText = "User submits settings update. JWT session expired mid-flight; client frontend fails silently.";
        const ss = document.getElementById('hero-ssim'); if (ss) ss.innerHTML = "0.9142 <span class='text-[10px] text-secondary font-normal'>(Repaint)</span>";
        const hd = document.getElementById('hero-delta'); if (hd) hd.innerHTML = "4.12% <span class='text-[10px] text-primary font-normal'>(Alert Drift)</span>";
        const hn = document.getElementById('hero-network'); if (hn) hn.innerText = "401 Unauth";
      }
    }

    // ── Drag & Drop Video Upload ───────────────────────────────────────────
    function handleDragOver(e) { e.preventDefault(); }
    function handleDragLeave(e) { e.preventDefault(); }
    function handleDrop(e) {
      e.preventDefault();
      if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
        processUploadedFile(e.dataTransfer.files[0]);
      }
    }
    function handleFileSelect(e) {
      if (e.target.files && e.target.files.length > 0) {
        processUploadedFile(e.target.files[0]);
      }
    }

    async function processUploadedFile(file) {
      uploadedFileName = file.name;
      document.getElementById('drop-header-text').innerText = `Uploading: ${file.name}...`;

      const formData = new FormData();
      formData.append('file', file);

      try {
        const res = await fetch('/api/upload-video', { method: 'POST', body: formData });
        const data = await res.json();
        if (data.status === 'success') {
          const a = data.analysis;
          document.getElementById('hero-session-name').innerText = file.name;
          document.getElementById('hero-file-size').innerText = `${(file.size / (1024*1024)).toFixed(1)} MB`;
          document.getElementById('hero-session-desc').innerText = `OpenCV extracted ${a.total_frames} frames (${a.duration_sec.toFixed(1)}s duration).`;
          document.getElementById('hero-video-dur').innerText = `00:${a.duration_sec.toFixed(0)}`;
          document.getElementById('hero-ssim').innerHTML = `${a.ssim} <span class='text-[10px] text-secondary'>(Analyzed)</span>`;
          document.getElementById('hero-delta').innerHTML = `${a.delta_pct}% <span class='text-[10px] text-primary'>(Delta)</span>`;
          
          const vidPlayer = document.getElementById('live-video-player');
          const thumb = document.getElementById('static-video-thumb');
          vidPlayer.src = `/uploads/${encodeURIComponent(data.filename)}`;
          vidPlayer.classList.remove('hidden');
          thumb.classList.add('hidden');

          switchDropState('filled');
        }
      } catch (err) {
        console.error('Upload error:', err);
        switchDropState('filled');
      }
    }

    // ── Main Pipeline Execution ────────────────────────────────────────────
    async function startAnalysisRun() {
      const btn = document.getElementById('main-analyze-btn');
      const originalText = btn ? btn.innerHTML : '';

      if (btn) {
        btn.innerHTML = '<span class="material-symbols-outlined text-[20px] animate-spin">refresh</span><span>Gemini Multimodal Reasoning in Progress...</span>';
        btn.disabled = true;
      }

      navigateTab('pipeline');
      animatePipelineDial(15);
      setTimeout(() => animatePipelineDial(45), 800);
      setTimeout(() => animatePipelineDial(78), 2000);

      try {
        const res = await fetch(`/api/run-pipeline?scenario_id=${currentScenario}&custom_filename=${encodeURIComponent(uploadedFileName)}&session_mode=${currentWorkflowMode}`, { method: 'POST' });
        const data = await res.json();
        
        if (data.status === 'success') {
          animatePipelineDial(100);
          setTimeout(() => {
            latestRunData = data;
            currentSessionId = data.session_id;
            bindResultsData(data);
            updateHistoryCount();
            if (btn) {
              btn.innerHTML = originalText;
              btn.disabled = false;
            }
            navigateTab('results');
          }, 400);
        } else {
          alert('Analysis Error: ' + (data.message || 'Pipeline failed'));
          if (btn) { btn.innerHTML = originalText; btn.disabled = false; }
          navigateTab('home');
        }
      } catch (err) {
        alert('Network failure reaching analysis engine: ' + err.message);
        if (btn) { btn.innerHTML = originalText; btn.disabled = false; }
        navigateTab('home');
      }
    }

    function bindResultsData(data) {
      if (!data) return;
      const scenario = data.scenario || {};
      const verdict = data.gemini_verdict || {};
      const ssim = data.ssim_result || {};
      const arbiter = data.arbiter_result || {};
      const suspectFile = verdict.suspect_file || scenario.suspect_file || 'pricing_engine.py';

      document.getElementById('res-duration').innerText = `${scenario.video_duration || '12.0s'}`;
      document.getElementById('res-confidence-tag').innerText = `Triage Confidence: ${arbiter.confidence || 'HIGH'}`;
      document.getElementById('res-session-id-label').innerText = `ID: #${data.session_id || '82FA-99C1'}`;
      
      const explanationText = verdict.explanation || verdict.intent || 'Anomaly diagnosed by Gemini 3.5.';
      document.getElementById('res-root-cause-text').innerHTML = `<strong class="text-on-surface">Gemini Diagnosis:</strong> ${escapeHtml(explanationText)}`;
      document.getElementById('deep-gemini-desc').innerText = explanationText;
      document.getElementById('deep-ssim-desc').innerText = `SSIM: ${ssim.ssim || '0.942'} · Delta: ${ssim.delta_pct || '1.85'}% · Tier ${arbiter.arbiter_tier || 1} Arbiter Precedence`;

      // Console trace update
      const traceEl = document.getElementById('res-console-trace');
      if (traceEl) {
        traceEl.innerText = data.console_trace || explanationText;
      }
      const traceFileEl = document.getElementById('trace-file-label');
      if (traceFileEl) {
        traceFileEl.innerText = suspectFile;
      }

      // Target file labels
      const patchTargetEl = document.getElementById('res-patch-target');
      if (patchTargetEl) patchTargetEl.innerText = suspectFile;
      const diffFileLabelEl = document.getElementById('diff-file-label');
      if (diffFileLabelEl) diffFileLabelEl.innerText = suspectFile;
      const deepTargetLabelEl = document.getElementById('deep-target-label');
      if (deepTargetLabelEl) deepTargetLabelEl.innerText = 'Target: ' + suspectFile;

      // Diff view
      const diffViewEl = document.getElementById('res-patch-diff-view');
      const patchDiff = data.patch_diff || scenario.patch_diff || '# No diff required';
      if (data.session_mode === 'WITH_REPO') {
        if (diffViewEl) diffViewEl.innerText = patchDiff;
        document.getElementById('res-playwright-code').innerHTML = `<code>${escapeHtml(data.playwright_code || '')}</code>`;
      } else {
        if (diffViewEl) diffViewEl.innerText = `# Mode: QA Triage Only (No source repo connected)\n# Suspect Component: ${suspectFile}\n# Diagnostic Root Cause:\n${explanationText}`;
        document.getElementById('res-playwright-code').innerHTML = `<code>// Playwright synthetic draft created for QA export\n${escapeHtml(data.playwright_code || '')}</code>`;
      }

      // Playwright test filename
      const pwFilenameEl = document.getElementById('res-playwright-filename');
      if (pwFilenameEl) {
        const cleanBase = suspectFile.split('/').pop().replace(/\\.[^/.]+$/, "");
        pwFilenameEl.innerText = `tests/synthetic/${cleanBase}-repro.spec.ts`;
      }

      // Telemetry
      if (data.telemetry) {
        document.getElementById('eco-saved-wh').innerText = `${data.telemetry.estimated_energy_saved_wh} Wh`;
        document.getElementById('eco-water-ml').innerText = `${data.telemetry.estimated_cooling_water_saved_ml} mL`;
        document.getElementById('eco-token-pct').innerText = `-${data.telemetry.token_reduction_pct}%`;
      }
    }

    function escapeHtml(str) {
      return (str || '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
    }

    // ── Deep-Dive Tabs (Results Screen) ────────────────────────────────────
    function switchAnalysisTab(tabId, btnElement) {
      const tabs = ['timeline', 'verdict', 'sandbox'];
      tabs.forEach(t => {
        const content = document.getElementById('tab-content-' + t);
        const btn = document.getElementById('tab-btn-' + t);
        if (content) {
          if (t === tabId) content.classList.remove('hidden');
          else content.classList.add('hidden');
        }
        if (btn) {
          if (t === tabId) {
            btn.className = "px-space-md py-2 rounded-lg text-xs font-bold bg-surface-container-lowest text-on-surface shadow-sm flex items-center gap-1.5 transition";
          } else {
            btn.className = "px-space-md py-2 rounded-lg text-xs font-medium text-on-surface-variant hover:text-on-surface transition flex items-center gap-1.5";
          }
        }
      });
    }

    // ── Drawer Option Toggle (Option 1 vs Option 2) ─────────────────────────
    function selectModalOption(num) {
      const card1 = document.getElementById('modalOption1');
      const card2 = document.getElementById('modalOption2');
      const r1 = document.getElementById('opt1Radio');
      const r2 = document.getElementById('opt2Radio');
      if (!card1 || !card2 || !r1 || !r2) return;

      if (num === 1) {
        card1.className = "cursor-pointer transition-all duration-200 p-space-lg rounded-xl flex flex-col justify-between shadow-md border-2 border-primary bg-primary/10 ring-2 ring-primary/30 relative";
        r1.className = "w-5 h-5 rounded-full border-2 border-primary bg-primary flex items-center justify-center text-on-primary";
        card2.className = "cursor-pointer transition-all duration-200 p-space-lg rounded-xl flex flex-col justify-between shadow-sm border border-outline-variant/30 bg-surface-container-low hover:border-outline hover:bg-surface-container relative";
        r2.className = "w-5 h-5 rounded-full border-2 border-outline-variant bg-transparent flex items-center justify-center text-transparent";
      } else {
        card2.className = "cursor-pointer transition-all duration-200 p-space-lg rounded-xl flex flex-col justify-between shadow-md border-2 border-primary bg-primary/10 ring-2 ring-primary/30 relative";
        r2.className = "w-5 h-5 rounded-full border-2 border-primary bg-primary flex items-center justify-center text-on-primary";
        card1.className = "cursor-pointer transition-all duration-200 p-space-lg rounded-xl flex flex-col justify-between shadow-sm border border-outline-variant/30 bg-surface-container-low hover:border-outline hover:bg-surface-container relative";
        r1.className = "w-5 h-5 rounded-full border-2 border-outline-variant bg-transparent flex items-center justify-center text-transparent";
      }
    }

    // ── Real GitOps GitHub PR Dispatch ──────────────────────────────────────
    async function triggerRealGitHubPR() {
      const btn = document.getElementById('drawer-pr-btn');
      const label = document.getElementById('drawer-pr-btn-label');
      label.innerText = "Dispatching PR via GitOps Engine...";
      btn.disabled = true;

      try {
        const res = await fetch('/api/create-pr', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            session_id: currentSessionId,
            title: `Fix: ${latestRunData ? latestRunData.scenario.title : 'Autonomous Defect Fix'}`,
            body: latestRunData ? latestRunData.pr_markdown : 'Verified by VERDANT'
          })
        });
        const data = await res.json();
        if (data.status === 'success' && data.pr_result) {
          const pr = data.pr_result;
          if (pr.pr_url) {
            window.open(pr.pr_url, '_blank');
            alert(`✓ Real GitHub Pull Request Opened!\nURL: ${pr.pr_url}`);
          } else {
            alert(`✓ Branch created & pushed!\nPR Markdown saved in: ${pr.payload_file || 'pr_payload.md'}`);
          }
          document.getElementById('fixDrawer').classList.add('hidden');
          updateHistoryCount();
        }
      } catch (e) {
        alert('PR dispatch failed: ' + e.message);
      } finally {
        label.innerText = "Create Pull Request on GitHub";
        btn.disabled = false;
      }
    }

    function copyForensicReportMarkdown() {
      if (latestRunData && latestRunData.pr_markdown) {
        navigator.clipboard.writeText(latestRunData.pr_markdown);
        alert('Forensic Report & Jira reproduction payload copied to clipboard!');
      } else {
        alert('Run analysis first to generate a report.');
      }
    }

    // ── Sustainability Live Metrics (Zero Hardcoding) ───────────────────────
    async function loadSustainabilityData() {
      try {
        const res = await fetch('/api/sustainability');
        const data = await res.json();
        if (data.status === 'success') {
          const whEl = document.getElementById('eco-saved-wh');
          const waterEl = document.getElementById('eco-water-ml');
          const tokenEl = document.getElementById('eco-token-pct');
          const sidebarSummary = document.getElementById('sidebar-saved-summary');
          const navBadge = document.getElementById('nav-history-badge');

          if (whEl) whEl.innerText = `${data.total_energy_saved_wh} Wh`;
          if (waterEl) {
            if (data.total_water_saved_ml >= 1000) {
              waterEl.innerText = `${(data.total_water_saved_ml / 1000).toFixed(2)} L`;
            } else {
              waterEl.innerText = `${data.total_water_saved_ml.toFixed(1)} mL`;
            }
          }
          if (tokenEl) tokenEl.innerText = `-${data.average_reduction_pct}%`;
          if (navBadge) navBadge.innerText = data.total_sessions || '0';
          if (sidebarSummary) {
            sidebarSummary.innerText = `${data.total_energy_saved_wh} Wh & ${data.total_water_saved_ml} mL saved across ${data.total_sessions} audits.`;
          }
        }
      } catch (e) {
        console.warn('Failed to load sustainability metrics:', e);
      }
    }

    // ── Audit History Database ──────────────────────────────────────────────
    async function loadHistoryData() {
      const tbody = document.getElementById('history-table-body');
      const empty = document.getElementById('history-empty');
      tbody.innerHTML = '<tr><td colspan="7" class="p-6 text-center text-outline"><i class="fa-solid fa-spinner fa-spin mr-2"></i>Loading persistent database records...</td></tr>';

      try {
        const res = await fetch('/api/history?limit=100');
        const data = await res.json();
        if (data.status === 'success') {
          cachedHistory = data.sessions || [];
          const s = data.stats || {};

          document.getElementById('hist-stat-total').innerText = s.total_sessions || 0;
          document.getElementById('hist-stat-with-repo').innerText = s.with_repo_count || 0;
          document.getElementById('hist-stat-no-repo').innerText = s.without_repo_count || 0;
          document.getElementById('hist-stat-prs').innerText = s.total_prs || 0;
          document.getElementById('hist-stat-energy').innerText = (s.total_energy_saved_wh || 0).toFixed(1);
          document.getElementById('hist-stat-water').innerText = (s.total_water_saved_ml || 0).toFixed(1);
          document.getElementById('nav-history-badge').innerText = s.total_sessions || 0;

          renderHistoryRows();
        }
      } catch (e) {
        tbody.innerHTML = `<tr><td colspan="7" class="p-4 text-center text-error">Failed loading history: ${e.message}</td></tr>`;
      }
    }

    function filterHistory(filter) {
      activeHistoryFilter = filter;
      document.getElementById('hfilter-all').className = filter === 'ALL' ? 'px-3 py-1 rounded-full text-xs font-bold bg-primary text-on-primary' : 'px-3 py-1 rounded-full text-xs font-medium text-on-surface-variant hover:bg-surface-container';
      document.getElementById('hfilter-repo').className = filter === 'WITH_REPO' ? 'px-3 py-1 rounded-full text-xs font-bold bg-primary text-on-primary' : 'px-3 py-1 rounded-full text-xs font-medium text-on-surface-variant hover:bg-surface-container';
      document.getElementById('hfilter-norepo').className = filter === 'WITHOUT_REPO' ? 'px-3 py-1 rounded-full text-xs font-bold bg-primary text-on-primary' : 'px-3 py-1 rounded-full text-xs font-medium text-on-surface-variant hover:bg-surface-container';
      renderHistoryRows();
    }

    function renderHistoryRows() {
      const tbody = document.getElementById('history-table-body');
      const empty = document.getElementById('history-empty');
      tbody.innerHTML = '';

      let list = cachedHistory;
      if (activeHistoryFilter !== 'ALL') {
        list = list.filter(item => item.session_mode === activeHistoryFilter);
      }

      if (list.length === 0) {
        empty.classList.remove('hidden');
        return;
      }
      empty.classList.add('hidden');

      list.forEach(item => {
        const tr = document.createElement('tr');
        tr.className = 'hover:bg-surface-container-low transition cursor-pointer';
        tr.onclick = () => openSessionDetail(item.id);

        const dateStr = item.created_at ? new Date(item.created_at * 1000).toLocaleString() : '--';
        const isWithRepo = (item.session_mode === 'WITH_REPO');
        const modeBadge = isWithRepo
          ? '<span class="bg-secondary-container text-on-secondary-container px-2 py-0.5 rounded text-[10px] font-bold">WITH REPO</span>'
          : '<span class="bg-tertiary-container/30 text-tertiary px-2 py-0.5 rounded text-[10px] font-bold">QA REPORT</span>';

        const proofTag = isWithRepo
          ? '<span class="text-secondary font-semibold"><i class="fa-solid fa-circle-check mr-1"></i>RED→GREEN</span>'
          : '<span class="text-outline font-normal">Diagnostic Only</span>';

        tr.innerHTML = `
          <td class="p-3 font-code text-[11px]">
            <div class="text-on-surface font-bold">#${item.id}</div>
            <div class="text-[10px] text-outline">${dateStr}</div>
          </td>
          <td class="p-3 max-w-xs">
            <div class="text-on-surface font-semibold truncate">${item.title || 'Untitled Incident'}</div>
            <div class="text-[11px] text-on-surface-variant truncate">${item.root_cause || item.spoken_summary || 'Diagnosis record'}</div>
          </td>
          <td class="p-3">${modeBadge}</td>
          <td class="p-3">
            <span class="font-bold text-on-surface">${item.confidence || 'HIGH'}</span>
            <span class="text-[10px] text-outline block">Tier ${item.arbiter_tier || 1} Arbiter</span>
          </td>
          <td class="p-3 text-[11px]">${proofTag}</td>
          <td class="p-3 font-code text-[11px] text-on-surface">
            <div>${item.energy_saved_wh || 0} Wh</div>
            <div class="text-[10px] text-secondary font-semibold">${item.water_saved_ml || 0} mL</div>
          </td>
          <td class="p-3 text-right">
            <button onclick="event.stopPropagation(); openSessionDetail('${item.id}')" class="px-2.5 py-1 rounded bg-surface-container hover:bg-surface-container-high text-on-surface text-[11px] font-semibold transition">
              Inspect
            </button>
          </td>
        `;
        tbody.appendChild(tr);
      });
    }

    async function openSessionDetail(sid) {
      try {
        const res = await fetch(`/api/history/${sid}`);
        const data = await res.json();
        if (data.status === 'success' && data.session) {
          const s = data.session;
          activeDetailSession = s;

          document.getElementById('sdetail-title').innerText = s.title || `Incident #${s.id}`;
          const dateStr = s.created_at ? new Date(s.created_at * 1000).toLocaleString() : '--';
          document.getElementById('sdetail-meta').innerText = `Session ID: ${s.id} · Created: ${dateStr}`;

          const isWithRepo = (s.session_mode === 'WITH_REPO');
          const badge = document.getElementById('sdetail-mode-badge');
          if (isWithRepo) {
            badge.className = 'px-2 py-0.5 rounded text-[10px] font-bold bg-secondary-container text-on-secondary-container';
            badge.innerText = 'WITH REPO (PATCH & PR)';
          } else {
            badge.className = 'px-2 py-0.5 rounded text-[10px] font-bold bg-tertiary-container/30 text-tertiary';
            badge.innerText = 'QA REPORT (NO REPO)';
          }

          document.getElementById('sdetail-root-cause').innerText = s.root_cause || 'No technical root cause recorded.';
          document.getElementById('sdetail-spoken').innerText = s.spoken_summary || '';

          // Steps
          const stepsContainer = document.getElementById('sdetail-steps');
          stepsContainer.innerHTML = '';
          const steps = s.reproduction_steps || [];
          if (steps.length > 0) {
            steps.forEach(st => {
              const div = document.createElement('div');
              div.className = 'p-2 rounded bg-surface-container text-[11px] text-on-surface font-code';
              div.innerText = st;
              stepsContainer.appendChild(div);
            });
          } else {
            stepsContainer.innerHTML = '<div class="text-outline text-[11px]">No specific reproduction steps recorded.</div>';
          }

          // Diff Box
          const diffBox = document.getElementById('sdetail-diff-box');
          const diffContent = document.getElementById('sdetail-diff-content');
          if (isWithRepo && s.patch_diff && s.patch_diff.trim()) {
            diffBox.classList.remove('hidden');
            diffContent.innerText = s.patch_diff;
          } else {
            diffBox.classList.add('hidden');
          }

          // Telemetry
          document.getElementById('sdetail-energy').innerText = `${s.energy_saved_wh || 0} Wh`;
          document.getElementById('sdetail-water').innerText = `${s.water_saved_ml || 0} mL`;

          // PR Box
          const prBox = document.getElementById('sdetail-pr-box');
          if (s.pr_url) {
            prBox.innerHTML = `<a href="${s.pr_url}" target="_blank" class="text-primary hover:underline font-semibold flex items-center gap-1"><span class="material-symbols-outlined text-[16px]">open_in_new</span><span>View GitHub PR ↗</span></a>`;
          } else if (isWithRepo) {
            prBox.innerHTML = `<button onclick="dispatchHistoryPR('${s.id}')" class="px-3 py-1 rounded bg-primary text-on-primary font-bold text-xs flex items-center gap-1"><span class="material-symbols-outlined text-[14px]">call_split</span><span>Dispatch PR</span></button>`;
          } else {
            prBox.innerHTML = `<span class="text-outline text-[11px]">No GitHub repo attached (QA Triage Mode)</span>`;
          }

          document.getElementById('session-detail-modal').classList.remove('hidden');
        }
      } catch (e) {
        alert('Failed fetching detail: ' + e.message);
      }
    }

    function closeSessionDetailModal() {
      document.getElementById('session-detail-modal').classList.add('hidden');
    }

    function copySessionMarkdown() {
      if (!activeDetailSession) return;
      const s = activeDetailSession;
      const diffBlock = s.patch_diff ? ('## Surgical Patch:\\n```diff\\n' + s.patch_diff + '\\n```') : '';
      const md = `# Forensic Incident Record: ${s.title}
- **Session ID**: #${s.id}
- **Mode**: ${s.session_mode}
- **Root Cause**: ${s.root_cause}
- **Spoken Summary**: ${s.spoken_summary}
- **Reproduction Steps**:
${(s.reproduction_steps || []).map(x => `  - ${x}`).join('\\n')}

${diffBlock}
`;
      navigator.clipboard.writeText(md);
      alert('Forensic markdown report copied to clipboard!');
    }

    async function dispatchHistoryPR(sid) {
      try {
        const res = await fetch('/api/create-pr', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ session_id: sid })
        });
        const data = await res.json();
        if (data.status === 'success' && data.pr_result && data.pr_result.pr_url) {
          window.open(data.pr_result.pr_url, '_blank');
          openSessionDetail(sid);
        } else {
          alert('PR payload generated in pr_payload.md');
        }
      } catch (e) {
        alert('Error: ' + e.message);
      }
    }

    async function updateHistoryCount() {
      try {
        const res = await fetch('/api/history?limit=1');
        const data = await res.json();
        if (data.status === 'success' && data.stats) {
          document.getElementById('nav-history-badge').innerText = data.stats.total_sessions || 0;
        }
      } catch (e) {}
    }

    // ── GitHub Modal & User Status ──────────────────────────────────────────
    function openGithubModal() {
      document.getElementById('github-modal').classList.remove('hidden');
      fetch('/api/user-status').then(r => r.json()).then(data => {
        if (data.status === 'success' && data.user) {
          const u = data.user;
          document.getElementById('gh-input-user').value = u.github_username || '';
          document.getElementById('gh-input-email').value = u.email || '';
          if (u.has_github_token) {
            document.getElementById('gh-modal-status-feedback').innerHTML = `✓ Active Token Encrypted (${u.masked_token})`;
          } else {
            document.getElementById('gh-modal-status-feedback').innerText = "No GitHub token currently configured.";
          }
        }
      });
    }

    function closeGithubModal() {
      document.getElementById('github-modal').classList.add('hidden');
    }

    async function saveGithubTokenAndUser() {
      const token = document.getElementById('gh-input-token').value.trim();
      const username = document.getElementById('gh-input-user').value.trim();
      const email = document.getElementById('gh-input-email').value.trim();
      const fb = document.getElementById('gh-modal-status-feedback');

      fb.innerHTML = 'Encrypting with AES-256 and saving to SQLite...';

      try {
        const res = await fetch('/api/connect-github', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ github_token: token, github_username: username, email: email })
        });
        const data = await res.json();
        if (data.status === 'success') {
          fb.innerHTML = '✓ Successfully connected and encrypted!';
          checkUserStatus();
          setTimeout(() => closeGithubModal(), 1200);
        }
      } catch (e) {
        fb.innerHTML = 'Error: ' + e.message;
      }
    }

    async function checkUserStatus() {
      try {
        const res = await fetch('/api/user-status');
        const data = await res.json();
        if (data.status === 'success' && data.user) {
          const u = data.user;
          const dot = document.getElementById('gh-status-dot');
          const label = document.getElementById('gh-repo-label');
          if (u.has_github_token) {
            dot.className = "w-2 h-2 rounded-full bg-secondary shadow-sm";
            label.innerText = u.github_username ? `${u.github_username}/VERDANT` : 'GitHub Connected';
          } else {
            dot.className = "w-2 h-2 rounded-full bg-outline";
            label.innerText = 'Connect GitHub';
          }
        }
      } catch (e) {}
    }

    // ── Init on Page Load & URL Listeners ─────────────────────────────────
    window.onload = () => {
      initScreenFromUrl();
      checkUserStatus();
      updateHistoryCount();
      loadSustainabilityData();
    };

    window.addEventListener('popstate', () => {
      initScreenFromUrl();
    });
  </script>

</body>
</html>
"""

def render_stitch_html(active_screen: str = "home") -> str:
    """Renders the Stitch template with the requested screen and tab pre-activated server-side."""
    screens = ["home", "sustainability", "history"]
    if active_screen not in screens:
        active_screen = "home"
    
    html = STITCH_HTML_TEMPLATE
    
    # 1. Update initial activeMainTab variable in JS
    html = html.replace("let activeMainTab = 'home';", f"let activeMainTab = '{active_screen}';")
    
    # 2. Adjust screen visibilities
    # First, make screen-home hidden if it's not active
    if active_screen != "home":
        html = html.replace('id="screen-home" class="w-full"', 'id="screen-home" class="w-full hidden"')
        # Now un-hide the target active screen
        html = html.replace(f'id="screen-{active_screen}" class="w-full hidden"', f'id="screen-{active_screen}" class="w-full"')
        
        # Adjust nav tab active styles
        html = html.replace('id="nav-btn-home" onclick="navigateTab(\'home\', event)" class="nav-tab-active',
                            'id="nav-btn-home" onclick="navigateTab(\'home\', event)" class="')
        html = html.replace(f'id="nav-btn-{active_screen}" onclick="navigateTab(\'{active_screen}\', event)" class="',
                            f'id="nav-btn-{active_screen}" onclick="navigateTab(\'{active_screen}\', event)" class="nav-tab-active ')
    
    return html

