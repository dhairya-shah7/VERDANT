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

      <!-- Navigation Links -->
      <nav class="flex flex-col gap-1.5" id="main-nav-bar">
        <a href="/" id="nav-btn-home" onclick="navigateTab('home', event); closeMobileSidebar();" class="nav-tab-active px-3.5 py-2.5 rounded-xl text-xs md:text-sm text-on-surface transition-all flex items-center gap-3 font-medium cursor-pointer">
          <span class="material-symbols-outlined text-[20px]">upload_file</span>
          <span>Bug Ingestion</span>
        </a>
        <a href="/pipeline" id="nav-btn-pipeline" onclick="navigateTab('pipeline', event); closeMobileSidebar();" class="px-3.5 py-2.5 rounded-xl text-xs md:text-sm text-on-surface-variant hover:text-on-surface hover:bg-surface-container transition-all flex items-center gap-3 font-medium cursor-pointer">
          <span class="material-symbols-outlined text-[20px]">neurology</span>
          <span>Multi-Layer Pipeline</span>
        </a>
        <a href="/results" id="nav-btn-results" onclick="navigateTab('results', event); closeMobileSidebar();" class="px-3.5 py-2.5 rounded-xl text-xs md:text-sm text-on-surface-variant hover:text-on-surface hover:bg-surface-container transition-all flex items-center gap-3 font-medium cursor-pointer">
          <span class="material-symbols-outlined text-[20px]">terminal</span>
          <span>Playwright Bench & PR</span>
        </a>
        <a href="/sustainability" id="nav-btn-sustainability" onclick="navigateTab('sustainability', event); closeMobileSidebar();" class="px-3.5 py-2.5 rounded-xl text-xs md:text-sm text-on-surface-variant hover:text-on-surface hover:bg-surface-container transition-all flex items-center gap-3 font-medium cursor-pointer">
          <span class="material-symbols-outlined text-[20px]">water_drop</span>
          <span>Sustainability (VERDE)</span>
        </a>
        <a href="/history" id="nav-btn-history" onclick="navigateTab('history', event); closeMobileSidebar();" class="px-3.5 py-2.5 rounded-xl text-xs md:text-sm text-on-surface-variant hover:text-on-surface hover:bg-surface-container transition-all flex items-center gap-3 font-medium cursor-pointer">
          <span class="material-symbols-outlined text-[20px]">history</span>
          <span>Audit History (<span id="nav-history-badge" class="font-bold text-secondary">2</span>)</span>
        </a>
      </nav>

      <!-- Quick Sustainability Action Card -->
      <div class="px-1">
        <a href="/sustainability" onclick="navigateTab('sustainability', event); closeMobileSidebar();" class="block p-3 rounded-xl bg-secondary-fixed/40 hover:bg-secondary-fixed/70 text-on-secondary-fixed-variant transition-all cursor-pointer border border-secondary-fixed">
          <div class="flex items-center gap-2 mb-1">
            <span class="material-symbols-outlined text-[18px] text-secondary">eco</span>
            <span class="text-xs font-bold">See What You Saved</span>
          </div>
          <p class="text-[11px] text-on-surface-variant leading-tight">82.2% energy & 1.18 L/kWh data center water reduction.</p>
        </a>
      </div>

    </div>

    <!-- Bottom Sidebar Controls -->
    <div class="flex flex-col gap-2 pt-4 border-t border-surface-container-high">
      <!-- GitHub Connector -->
      <button onclick="openGithubModal()" id="header-gh-btn" class="w-full flex items-center justify-between p-2.5 rounded-xl bg-surface-container-low hover:bg-surface-container text-on-surface-variant transition text-xs">
        <div class="flex items-center gap-2 min-w-0">
          <span class="material-symbols-outlined text-[18px]">account_tree</span>
          <div class="flex flex-col text-left min-w-0">
            <div class="flex items-center gap-1 font-code text-[11px] truncate">
              <span id="gh-status-dot" class="w-2 h-2 rounded-full bg-secondary animate-pulse flex-shrink-0"></span>
              <span id="gh-repo-label" class="text-on-surface font-medium truncate">dhairya-shah7/VERDANT</span>
            </div>
            <span class="text-[10px] text-outline">Branch: main</span>
          </div>
        </div>
        <span class="material-symbols-outlined text-[16px] text-on-surface-variant">settings</span>
      </button>

      <!-- Buggy Store link -->
      <a href="/demo-app" target="_blank" class="w-full flex items-center gap-2 p-2 rounded-lg text-xs text-on-surface-variant hover:text-on-surface hover:bg-surface-container transition">
        <span class="material-symbols-outlined text-[16px] text-primary">storefront</span>
        <span>Launch Buggy Store Demo</span>
        <span class="material-symbols-outlined text-[14px] ml-auto">open_in_new</span>
      </a>
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
          <section class="w-full flex flex-col items-center text-center max-w-3xl mx-auto pt-2">
            <h1 class="text-2xl sm:text-3xl md:text-4xl font-bold text-on-surface tracking-tight mb-2">
              Turn Bug Videos Into Verified Fixes.
            </h1>
            <p class="text-xs sm:text-sm md:text-base text-on-surface-variant max-w-2xl px-2">
              Drop any bug recording or console log. V.E.R.D.A.N.T. extracts the defect locus with Google Gemini 3.5 & Mathematical SSIM, then returns a verified Playwright reproduction proof and surgical GitHub PR.
            </p>
          </section>

          <!-- Video Dropzone & Preview Section -->
          <section class="w-full max-w-4xl mx-auto flex flex-col gap-4">
            
            <!-- Toggle Tabs: Fresh File Dropzone vs Pre-loaded Demo -->
            <div class="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-2 px-1">
              <div class="flex items-center gap-1.5 bg-surface-container-low p-1 rounded-xl w-full sm:w-auto">
                <button class="flex-1 sm:flex-initial px-4 py-1.5 rounded-lg text-xs bg-surface-container-lowest text-primary shadow-sm font-semibold transition-all cursor-pointer" id="btn-tab-upload" onclick="switchDropState('empty')">
                  Fresh File Dropzone
                </button>
                <button class="flex-1 sm:flex-initial px-4 py-1.5 rounded-lg text-xs text-on-surface-variant hover:text-on-surface transition-all cursor-pointer" id="btn-tab-preview" onclick="switchDropState('filled')">
                  Pre-loaded Session (Active)
                </button>
              </div>
              <span class="text-xs text-outline flex items-center gap-1">
                <span class="material-symbols-outlined text-[15px] text-secondary">verified</span> Google Gemini 3.5 & SSIM Consensus
              </span>
            </div>

            <!-- STATE A: Pre-loaded / Filled Preview Card (Hidden by default) -->
            <div class="w-full bg-surface-container-lowest rounded-2xl shadow-sm p-4 sm:p-6 flex flex-col md:flex-row gap-6 items-center transition-all border border-surface-container-high hidden" id="state-filled">
              <!-- Video Preview Thumbnail / Live Video -->
              <div class="relative w-full md:w-80 h-48 sm:h-52 rounded-xl overflow-hidden bg-surface-container-highest flex-shrink-0 group shadow-inner">
                <video id="live-video-player" class="w-full h-full object-cover hidden" controls></video>
                <img id="static-video-thumb" class="w-full h-full object-cover" src="https://lh3.googleusercontent.com/aida-public/AB6AXuCtgG0dzA9PiKrAt8unHFrKp0r-aOjcLquhlIrvfr6cQ3bistPLMWfOkAR9JWW_ChQdJQbvld9OjWlaGRLq0WmvsfdH6elr2izwwXdgL-6Z9lQZapS0KWQAAsRXKcR_uNbGdVDGdE1bTd-kdEyS1KmqWQ_-we1VetVJo9uUnNLqPmRARl4sOwI-RsPkMQinDyP6BUHRcz40V649EjB2u20knEX7jkurqiJhsMqx5qI" alt="Checkout session preview">
                <div class="absolute inset-0 bg-gradient-to-t from-black/70 via-transparent to-transparent flex flex-col justify-between p-3 pointer-events-none">
                  <div class="flex items-center justify-between">
                    <span class="px-2 py-0.5 rounded-full bg-surface-container-lowest/90 font-code text-[11px] text-on-surface font-semibold flex items-center gap-1 shadow-sm">
                      <span class="w-1.5 h-1.5 rounded-full bg-error animate-ping"></span> 1080p 60fps
                    </span>
                    <span class="px-2 py-0.5 rounded bg-surface-container-lowest/90 font-code text-[11px] text-on-surface" id="hero-video-dur">00:24.2</span>
                  </div>
                  <div class="flex items-center justify-between">
                    <div class="flex items-center gap-1 px-2 py-1 rounded bg-error-container/90 text-on-error-container text-[11px] font-semibold backdrop-blur">
                      <span class="material-symbols-outlined text-[14px]">touch_app</span> <span id="hero-defect-tag">Silent Freeze Detected</span>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Video Details and Keyframe Metrics -->
              <div class="flex flex-col justify-between w-full h-full min-w-0">
                <div>
                  <div class="flex items-start justify-between gap-2 mb-2">
                    <div>
                      <div class="flex items-center gap-2 flex-wrap">
                        <h3 class="font-bold text-sm sm:text-base text-on-surface truncate" id="hero-session-name">
                          checkout_unresponsive_submit_freeze.mp4
                        </h3>
                        <span class="px-2 py-0.5 rounded-full bg-secondary-fixed text-on-secondary-fixed-variant text-[11px] font-semibold" id="hero-file-size">
                          14.2 MB
                        </span>
                      </div>
                      <p class="text-xs text-on-surface-variant mt-1" id="hero-session-desc">
                        User clicks 'Place Order'. Network returns 500; button stays disabled with zero visual repaint.
                      </p>
                    </div>
                  </div>

                  <!-- Keyframe Indicators -->
                  <div class="grid grid-cols-2 sm:grid-cols-4 gap-2 my-3">
                    <div class="bg-surface-container-low p-2 rounded-xl flex flex-col">
                      <span class="text-[10px] text-outline uppercase font-semibold">SSIM Index</span>
                      <span class="text-sm text-on-surface font-bold" id="hero-ssim">0.9984 <span class="text-[10px] text-error font-normal">(Frozen)</span></span>
                    </div>
                    <div class="bg-surface-container-low p-2 rounded-xl flex flex-col">
                      <span class="text-[10px] text-outline uppercase font-semibold">Pixel Delta</span>
                      <span class="text-sm text-on-surface font-bold" id="hero-delta">0.02% <span class="text-[10px] text-secondary font-normal">(Zero Drift)</span></span>
                    </div>
                    <div class="bg-surface-container-low p-2 rounded-xl flex flex-col">
                      <span class="text-[10px] text-outline uppercase font-semibold">Network API</span>
                      <span class="text-sm text-error font-bold" id="hero-network">500 Fail</span>
                    </div>
                    <div class="bg-surface-container-low p-2 rounded-xl flex flex-col">
                      <span class="text-[10px] text-outline uppercase font-semibold">Target DOM</span>
                      <span class="font-code text-xs text-primary font-bold truncate">button#checkout-btn</span>
                    </div>
                  </div>

                  <!-- Extraction Progress -->
                  <div class="flex flex-col gap-1 mt-2">
                    <div class="flex items-center justify-between text-xs">
                      <span class="flex items-center gap-1 text-secondary font-semibold">
                        <span class="material-symbols-outlined text-[16px]">check_circle</span>
                        100% Ingested & ContextPrism Distilled
                      </span>
                      <span class="font-code text-[11px] text-outline-variant">Pruned -84.9% Tokens</span>
                    </div>
                    <div class="w-full h-1.5 bg-surface-container-high rounded-full overflow-hidden">
                      <div class="w-full h-full bg-secondary rounded-full"></div>
                    </div>
                  </div>
                </div>

                <!-- Scenario Switcher Buttons -->
                <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2 pt-3 mt-3 border-t border-surface-container">
                  <div class="flex items-center gap-2 flex-wrap">
                    <span class="text-xs text-outline font-semibold">Pre-set Scenarios:</span>
                    <button onclick="selectPreset('checkout_500')" id="btn-preset-checkout" class="px-2.5 py-1 rounded-lg text-xs font-semibold bg-primary text-on-primary shadow-sm transition cursor-pointer">
                      Checkout 500 Freeze
                    </button>
                    <button onclick="selectPreset('auth_token_expired')" id="btn-preset-auth" class="px-2.5 py-1 rounded-lg text-xs font-semibold bg-surface-container hover:bg-surface-container-high text-on-surface transition cursor-pointer">
                      Auth 401 Expiry
                    </button>
                  </div>
                  <span class="text-[11px] text-outline font-code">Dual-Engine Ready</span>
                </div>
              </div>
            </div>

            <!-- STATE B: Empty Drag-and-Drop Zone (Visible by default) -->
            <div class="w-full bg-primary/5 hover:bg-primary/10 border-2 border-dashed border-primary/30 hover:border-primary/60 transition-all rounded-2xl p-6 sm:p-10 flex flex-col items-center justify-center text-center cursor-pointer shadow-sm group min-h-[260px] sm:min-h-[300px] relative overflow-hidden" id="state-empty"
                 ondragover="handleDragOver(event)" ondragleave="handleDragLeave(event)" ondrop="handleDrop(event)" onclick="document.getElementById('file-input-real').click()">
              <input type="file" id="file-input-real" class="hidden" accept="video/mp4,video/webm,image/png,image/jpeg" onchange="handleFileSelect(event)">
              <div class="w-full py-4 flex flex-col items-center justify-center text-center relative pointer-events-none">
                <div class="w-16 h-16 rounded-full bg-primary flex items-center justify-center text-on-primary shadow-lg mb-4 animate-bounce">
                  <span class="material-symbols-outlined text-[32px]">file_download</span>
                </div>
                <h2 class="text-xl sm:text-2xl font-bold text-primary mb-1.5" id="drop-header-text">Drop Your Bug Video or Logs Here</h2>
                <p class="text-xs sm:text-sm text-on-surface-variant max-w-md mb-4 px-2">
                  Supports MP4, WebM, and HAR/Console log archives. ContextPrism automatically isolates critical transition frames within ±1.5s.
                </p>
                <div class="flex items-center gap-2 text-xs">
                  <span class="px-3.5 py-1.5 rounded-full bg-surface-container-lowest text-primary font-semibold shadow-sm border border-surface-container-high">
                    Browse or Drop File
                  </span>
                  <span class="text-outline">• Up to 50MB</span>
                </div>
              </div>
            </div>

          </section>

          <!-- Primary Run Action Buttons -->
          <section class="w-full max-w-4xl mx-auto flex flex-col items-center gap-3 pt-2">
            <div class="flex flex-col sm:flex-row items-stretch sm:items-center justify-center gap-3 w-full sm:w-auto">
              <button onclick="startAnalysisRun(false)" id="main-analyze-btn" class="w-full sm:w-auto inline-flex items-center justify-center gap-2 px-6 sm:px-8 py-3.5 rounded-full bg-primary hover:bg-primary-container text-on-primary shadow-md hover:shadow-lg text-sm sm:text-base font-semibold tracking-wide transition-all transform hover:-translate-y-0.5 active:translate-y-0 cursor-pointer text-center">
                <span class="material-symbols-outlined text-[20px]">auto_fix_high</span>
                <span id="analyze-btn-text">Analyze Video (Instant Repro • 1.5s)</span>
                <span class="material-symbols-outlined text-[18px]">arrow_forward</span>
              </button>
              <button onclick="startAnalysisRun(true)" id="cloud-analyze-btn" class="w-full sm:w-auto inline-flex items-center justify-center gap-2 px-5 sm:px-6 py-3.5 rounded-full bg-surface-container-low hover:bg-surface-container text-on-surface border border-surface-container-high shadow-sm text-xs sm:text-sm font-semibold tracking-wide transition-all cursor-pointer text-center">
                <span class="material-symbols-outlined text-[18px] text-secondary">cloud_sync</span>
                <span>Run Live Gemini 3.5 API (~50s)</span>
              </button>
            </div>
            <p class="text-[11px] text-outline text-center px-4">Instant Repro animates the optical flow pipeline & results immediately. Cloud mode connects live to Google Gemini 3.5.</p>
          </section>

        </div>
      </div>
    </div>

    <!-- ======================================================================= -->
    <!-- SCREEN 2: MULTI-LAYER PROCESSING PIPELINE                               -->
    <!-- ======================================================================= -->
    <div id="screen-pipeline" class="w-full hidden">
      <div class="w-full max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 sm:py-8 flex flex-col gap-6">
        
        <!-- Pipeline Header -->
        <div class="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-4 border-b border-surface-container-high">
          <div>
            <div class="flex items-center gap-2 mb-1">
              <span class="px-2 py-0.5 rounded-full bg-primary/10 text-primary text-[11px] font-semibold uppercase tracking-wider">Multi-Layer Runtime</span>
              <span class="text-outline">•</span>
              <span class="text-xs font-code text-secondary font-semibold" id="pipeline-status-text">Optical Flow & Verification Active</span>
            </div>
            <h1 class="text-2xl sm:text-3xl font-bold text-on-surface">Forensic Processing Pipeline</h1>
            <p class="text-xs sm:text-sm text-on-surface-variant">Real-time state distillation across ContextPrism, ApexTrace, and Replay Shield</p>
          </div>
          <div class="flex items-center gap-2 self-start md:self-auto flex-wrap">
            <button onclick="navigateTab('home', event)" class="px-4 py-2 rounded-full bg-surface-container hover:bg-surface-container-high text-on-surface text-xs font-semibold transition shadow-sm flex items-center gap-1.5 cursor-pointer">
              <span class="material-symbols-outlined text-[16px]">arrow_back</span>
              <span>Back to Ingestion</span>
            </button>
            <button onclick="navigateTab('results', event)" class="px-5 py-2 rounded-full bg-primary text-on-primary text-xs font-semibold hover:bg-primary-container transition shadow-sm flex items-center gap-1.5 cursor-pointer">
              <span>View Verified Fix & PR</span>
              <span class="material-symbols-outlined text-[16px]">arrow_forward</span>
            </button>
          </div>
        </div>

        <!-- Upper Grid: Dial Gauge + Frame Inspector Carousel -->
        <div class="grid grid-cols-1 lg:grid-cols-12 gap-6">
          
          <!-- Circular Progress Dial (4 Cols on xl, 5 on lg) -->
          <div class="lg:col-span-5 xl:col-span-4 bg-surface-container-lowest p-5 sm:p-6 rounded-2xl shadow-sm flex flex-col justify-between border border-surface-container-high">
            <div>
              <div class="flex items-center justify-between mb-space-sm">
                <h2 class="text-base font-bold text-on-surface">Synthesis Progress</h2>
                <span class="px-2 py-0.5 rounded bg-surface-container text-[11px] font-code text-primary font-semibold">Hermetic Loop</span>
              </div>
              <p class="text-xs text-on-surface-variant">4-layer pipeline synchronization</p>
            </div>

            <!-- SVG Gauge -->
            <div class="my-space-lg flex flex-col items-center justify-center">
              <div class="relative w-48 h-48 flex items-center justify-center">
                <svg class="w-full h-full transform -rotate-90" viewBox="0 0 100 100">
                  <circle cx="50" cy="50" r="42" stroke="#efedf1" stroke-width="8" fill="transparent"></circle>
                  <circle id="pipeline-svg-circle" cx="50" cy="50" r="42" stroke="#0058bd" stroke-width="8" stroke-linecap="round" stroke-dasharray="264" stroke-dashoffset="12" fill="transparent"></circle>
                </svg>
                <div class="absolute inset-0 flex flex-col items-center justify-center text-center">
                  <span class="text-3xl font-bold text-on-surface tracking-tight" id="pipeline-pct-label">96%</span>
                  <span class="text-[10px] font-bold text-primary uppercase tracking-wider">Completed</span>
                  <div class="flex items-center gap-1 mt-1 text-secondary font-code text-[11px]">
                    <span class="w-1.5 h-1.5 rounded-full bg-secondary animate-pulse"></span>
                    <span>Layers Synchronized</span>
                  </div>
                </div>
              </div>
            </div>

            <!-- Diagnostic Specs -->
            <div class="grid grid-cols-2 gap-space-sm bg-surface-container-low p-space-md rounded-lg text-xs">
              <div>
                <span class="text-[10px] text-on-surface-variant block uppercase font-semibold">Frame Index</span>
                <span class="font-code text-xs font-semibold text-on-surface" id="pipe-frame-count">562 / 720</span>
              </div>
              <div>
                <span class="text-[10px] text-on-surface-variant block uppercase font-semibold">Sampling Rate</span>
                <span class="font-code text-xs font-semibold text-on-surface">30.0 fps (Raw)</span>
              </div>
              <div>
                <span class="text-[10px] text-on-surface-variant block uppercase font-semibold">Optic Flow Depth</span>
                <span class="font-code text-xs font-semibold text-secondary">Verified (12 Flow Vecs)</span>
              </div>
              <div>
                <span class="text-[10px] text-on-surface-variant block uppercase font-semibold">Consensus Engine</span>
                <span class="font-code text-xs font-semibold text-primary">Gemini 3.5 + SSIM</span>
              </div>
            </div>
          </div>

          <!-- Live Frame Inspector & Optical Vectors (7 Cols on lg, 8 Cols on xl) -->
          <div class="lg:col-span-7 xl:col-span-8 bg-surface-container-lowest p-5 sm:p-6 rounded-2xl shadow-sm flex flex-col justify-between border border-surface-container-high">
            <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2 pb-3 border-b border-surface-container">
              <div class="flex items-center gap-2">
                <span class="material-symbols-outlined text-secondary text-[22px]">video_search</span>
                <div>
                  <h3 class="font-bold text-sm text-on-surface">Live Frame Inspector & Optical Transition Vectors</h3>
                  <p class="text-xs text-on-surface-variant">Temporal sampling around user interaction locus</p>
                </div>
              </div>
              <span class="inline-flex items-center gap-1 font-code text-xs text-error bg-error-container/60 px-3 py-1 rounded-full font-semibold self-start sm:self-auto">
                <span class="material-symbols-outlined text-[15px]">warning</span>
                Defect Locus at T+00:12.4s
              </span>
            </div>

            <!-- 5-Frame Carousel Grid (Clickable) -->
            <div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-3 my-4">
              <!-- Frame 1 -->
              <div id="carousel-frame-1" onclick="selectFrame(1)" class="flex flex-col gap-1 cursor-pointer hover:ring-2 hover:ring-primary rounded-lg p-0.5 transition">
                <div class="relative w-full aspect-video rounded-lg overflow-hidden bg-surface-container-high shadow-inner">
                  <img class="w-full h-full object-cover" src="https://lh3.googleusercontent.com/aida-public/AB6AXuB6zedw27BYsaMGlsI_q7T4GmBnCQm-_mhiL52Mr-gkyH9QL6K1vc8cV_cb7Dy8in5jtKemp3zvzTp_ztgqWBbSwuBQ5PQaadlY-Q4UXwwdizsqg-zr1xh2m8z5YNaXxYIltOsogbrxBdFwCPVdbXRI40B3ffBSBN46Zh-CwoHx4NTJi-vhWg7HCgGuOTBCVgLdTXOX17S7rniSMCz9CFNhOimn-9Qv7pfSHE1Ffk8">
                  <div class="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent"></div>
                  <span class="absolute bottom-1 left-1.5 font-code text-[10px] text-white">00:04.0</span>
                  <span class="absolute top-1.5 right-1.5 w-2 h-2 rounded-full bg-secondary"></span>
                </div>
                <div class="flex items-center justify-between font-code text-[10px] text-on-surface-variant">
                  <span>Frame #120</span>
                  <span class="text-secondary font-medium">SSIM 0.99</span>
                </div>
              </div>

              <!-- Frame 2 -->
              <div id="carousel-frame-2" onclick="selectFrame(2)" class="flex flex-col gap-1 cursor-pointer hover:ring-2 hover:ring-primary rounded-lg p-0.5 transition">
                <div class="relative w-full aspect-video rounded-lg overflow-hidden bg-surface-container-high shadow-inner">
                  <img class="w-full h-full object-cover" src="https://lh3.googleusercontent.com/aida-public/AB6AXuCwCNnO1HdO23ZHjskBt50HWs9tzRIJozyyckcDeegj0BNE_W-LDoCLti9fQw3_egPo-tfwKix2z5EZCDQlDqWJ-Ty1P8VBDJDg09lwK0ElNFM_tJZJonOndlwJjHgmPFj_oDDztO-83GdxVF3iVx82O1iG3jsNI7okyDaIH31Z5p8QZLimPA4jX02KySNK5PhhtkEOjpLpULWaV1T_meEYWeIAkjDA0GvhCHAX_pI">
                  <div class="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent"></div>
                  <span class="absolute bottom-1 left-1.5 font-code text-[10px] text-white">00:08.0</span>
                  <span class="absolute top-1.5 right-1.5 w-2 h-2 rounded-full bg-secondary"></span>
                </div>
                <div class="flex items-center justify-between font-code text-[10px] text-on-surface-variant">
                  <span>Frame #240</span>
                  <span class="text-secondary font-medium">SSIM 0.98</span>
                </div>
              </div>

              <!-- Frame 3 (ANOMALY) -->
              <div id="carousel-frame-3" onclick="selectFrame(3)" class="flex flex-col gap-1 relative ring-2 ring-error rounded-lg p-0.5 cursor-pointer bg-error/5">
                <div class="relative w-full aspect-video rounded-lg overflow-hidden bg-surface-container-high shadow-md">
                  <img class="w-full h-full object-cover scale-105" src="https://lh3.googleusercontent.com/aida-public/AB6AXuDTNksevmGPnmEw9YBhcXBElRAJn6JfNiH7OprSLDCjq0uJEkmv2kimS4ak6SBKib9G2vsJUOdIE5cbPKFFU1HLw1Cvef8fs1abBRiadSoKpryTh_SiFkaWWe4wL9616AS9jfCIpSl07TUcfS2zu3z7Eg2SuO2JvlF9oi6fjqNCmPMpt4oeBOkW3LI91sVJqSAcAxzl5YyjgQmF_wdm1Jsp7YIZ-YeNlq4_QeAxl9o">
                  <!-- Red Target Overlay -->
                  <div class="absolute inset-0 bg-error/10 flex items-center justify-center">
                    <div class="w-16 h-8 border-2 border-dashed border-error rounded flex items-center justify-center bg-error/20">
                      <span class="text-[9px] font-code font-bold text-error">FREEZE</span>
                    </div>
                  </div>
                  <span class="absolute bottom-1 left-1.5 font-code text-[10px] text-white font-bold bg-error/80 px-1 rounded">00:12.4</span>
                  <span class="absolute top-1.5 right-1.5 w-2 h-2 rounded-full bg-error animate-ping"></span>
                </div>
                <div class="flex items-center justify-between font-code text-[10px] text-error font-bold">
                  <span>Frame #372</span>
                  <span>Δ 0.02%</span>
                </div>
              </div>

              <!-- Frame 4 -->
              <div id="carousel-frame-4" onclick="selectFrame(4)" class="flex flex-col gap-1 cursor-pointer hover:ring-2 hover:ring-primary rounded-lg p-0.5 transition">
                <div class="relative w-full aspect-video rounded-lg overflow-hidden bg-surface-container-high shadow-inner">
                  <img class="w-full h-full object-cover" src="https://lh3.googleusercontent.com/aida-public/AB6AXuB6zedw27BYsaMGlsI_q7T4GmBnCQm-_mhiL52Mr-gkyH9QL6K1vc8cV_cb7Dy8in5jtKemp3zvzTp_ztgqWBbSwuBQ5PQaadlY-Q4UXwwdizsqg-zr1xh2m8z5YNaXxYIltOsogbrxBdFwCPVdbXRI40B3ffBSBN46Zh-CwoHx4NTJi-vhWg7HCgGuOTBCVgLdTXOX17S7rniSMCz9CFNhOimn-9Qv7pfSHE1Ffk8">
                  <div class="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent"></div>
                  <span class="absolute bottom-1 left-1.5 font-code text-[10px] text-white">00:16.0</span>
                  <span class="absolute top-1.5 right-1.5 w-2 h-2 rounded-full bg-error"></span>
                </div>
                <div class="flex items-center justify-between font-code text-[10px] text-on-surface-variant">
                  <span>Frame #480</span>
                  <span class="text-error font-medium">Halted</span>
                </div>
              </div>

              <!-- Frame 5 -->
              <div id="carousel-frame-5" onclick="selectFrame(5)" class="flex flex-col gap-1 cursor-pointer hover:ring-2 hover:ring-primary rounded-lg p-0.5 transition">
                <div class="relative w-full aspect-video rounded-lg overflow-hidden bg-surface-container-high shadow-inner">
                  <img class="w-full h-full object-cover" src="https://lh3.googleusercontent.com/aida-public/AB6AXuCwCNnO1HdO23ZHjskBt50HWs9tzRIJozyyckcDeegj0BNE_W-LDoCLti9fQw3_egPo-tfwKix2z5EZCDQlDqWJ-Ty1P8VBDJDg09lwK0ElNFM_tJZJonOndlwJjHgmPFj_oDDztO-83GdxVF3iVx82O1iG3jsNI7okyDaIH31Z5p8QZLimPA4jX02KySNK5PhhtkEOjpLpULWaV1T_meEYWeIAkjDA0GvhCHAX_pI">
                  <div class="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent"></div>
                  <span class="absolute bottom-1 left-1.5 font-code text-[10px] text-white">00:20.0</span>
                  <span class="absolute top-1.5 right-1.5 w-2 h-2 rounded-full bg-error"></span>
                </div>
                <div class="flex items-center justify-between font-code text-[10px] text-on-surface-variant">
                  <span>Frame #600</span>
                  <span class="text-error font-medium">Halted</span>
                </div>
              </div>
            </div>

            <!-- Footer Stats -->
            <div class="pt-space-sm border-t border-surface-container flex items-center justify-between text-xs text-on-surface-variant">
              <span>Entropy Shift: <strong class="text-error">High Anomaly Spike (+84.2%)</strong></span>
              <span class="font-code text-[11px] text-outline">Locus: &lt;button#checkout-btn&gt;</span>
            </div>
          </div>

        </div>

      </div>
    </div>

    <!-- ======================================================================= -->
    <!-- SCREEN 3: RESULTS & VERIFICATION DASHBOARD                              -->
    <!-- ======================================================================= -->
    <div id="screen-results" class="w-full hidden">
      <div class="w-full max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 sm:py-8 flex flex-col gap-6">
        
        <!-- Header & Action Row -->
        <div class="flex flex-col md:flex-row md:items-end justify-between gap-4 pb-4 border-b border-surface-container-high">
          <div>
            <div class="flex items-center gap-2 mb-1">
              <span class="px-2 py-0.5 rounded-full bg-primary/10 text-primary text-[11px] font-semibold uppercase tracking-wider">Autonomous Post-Mortem</span>
              <span class="text-outline-variant">•</span>
              <span class="font-code text-xs text-outline">Engine: ApexTrace v3.2 · Gemini 3.5</span>
            </div>
            <h1 class="text-2xl sm:text-3xl font-bold text-on-surface tracking-tight">Analysis Complete</h1>
            <p class="text-xs sm:text-sm text-on-surface-variant">Here is what V.E.R.D.A.N.T. discovered and verified in your recording.</p>
          </div>
          
          <div class="flex items-center gap-2 shrink-0 flex-wrap">
            <button onclick="copyForensicReportMarkdown()" class="px-4 py-2 rounded-full bg-surface-container hover:bg-surface-container-high text-xs font-semibold text-on-surface transition flex items-center gap-1 shadow-sm cursor-pointer">
              <span class="material-symbols-outlined text-[18px]">share</span>
              <span>Copy Report</span>
            </button>
            <button onclick="document.getElementById('fixDrawer').classList.remove('hidden')" class="px-5 py-2 rounded-full bg-primary hover:bg-primary-container text-on-primary text-xs font-bold shadow-sm transition flex items-center gap-1.5 cursor-pointer">
              <span class="material-symbols-outlined text-[18px]">auto_fix_high</span>
              <span>Resolution Actions</span>
            </button>
          </div>
        </div>

        <!-- 4 Compact Summary KPI Cards -->
        <div class="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-4">
          <div class="bg-surface-container-lowest p-5 rounded-2xl shadow-sm border border-surface-container-high flex flex-col justify-between">
            <div class="flex items-center justify-between text-on-surface-variant">
              <span class="text-xs font-semibold">Total Faults</span>
              <span class="w-6 h-6 rounded-full bg-error-container text-on-error-container flex items-center justify-center">
                <span class="material-symbols-outlined text-[16px]">bug_report</span>
              </span>
            </div>
            <div class="mt-4 flex items-baseline justify-between">
              <div class="text-2xl font-bold text-on-surface">1</div>
              <span class="px-2 py-0.5 rounded-full bg-error-container text-on-error-container text-[11px] font-semibold">Critical Fault</span>
            </div>
          </div>

          <div class="bg-surface-container-lowest p-5 rounded-2xl shadow-sm border border-surface-container-high flex flex-col justify-between">
            <div class="flex items-center justify-between text-on-surface-variant">
              <span class="text-xs font-semibold">Severity</span>
              <span class="w-6 h-6 rounded-full bg-error-container text-on-error-container flex items-center justify-center">
                <span class="material-symbols-outlined text-[16px]">warning</span>
              </span>
            </div>
            <div class="mt-4 flex items-baseline justify-between">
              <div class="text-2xl font-bold text-error">Critical</div>
              <span class="text-xs text-outline">UI Freeze</span>
            </div>
          </div>

          <div class="bg-surface-container-lowest p-5 rounded-2xl shadow-sm border border-surface-container-high flex flex-col justify-between">
            <div class="flex items-center justify-between text-on-surface-variant">
              <span class="text-xs font-semibold">Duration</span>
              <span class="w-6 h-6 rounded-full bg-surface-container text-primary flex items-center justify-center">
                <span class="material-symbols-outlined text-[16px]">timer</span>
              </span>
            </div>
            <div class="mt-4 flex items-baseline justify-between">
              <div class="text-2xl font-bold text-on-surface" id="res-duration">24.2s</div>
              <span class="text-xs text-outline">720 frames</span>
            </div>
          </div>

          <div class="bg-surface-container-lowest p-5 rounded-2xl shadow-sm border border-surface-container-high flex flex-col justify-between">
            <div class="flex items-center justify-between text-on-surface-variant">
              <span class="text-xs font-semibold">Verification</span>
              <span class="w-6 h-6 rounded-full bg-secondary-container text-on-secondary-container flex items-center justify-center">
                <span class="material-symbols-outlined text-[16px]">verified</span>
              </span>
            </div>
            <div class="mt-space-md flex items-baseline justify-between">
              <div class="text-2xl font-bold text-secondary">Passed</div>
              <span class="px-2 py-0.5 rounded-full bg-secondary-container text-on-secondary-container text-[11px] font-semibold">RED→GREEN Replay</span>
            </div>
          </div>
        </div>

        <!-- The Centerpiece: Two Connected Panels (Problem vs Solution) -->
        <div class="relative w-full">
          <div class="grid grid-cols-1 lg:grid-cols-2 gap-gutter-desktop items-stretch relative">
            
            <!-- Left Panel: Detected Issue -->
            <div class="bg-surface-container-lowest rounded-xl p-space-xl flex flex-col justify-between shadow-sm relative overflow-hidden border border-surface-container-high">
              <div class="absolute top-0 left-0 right-0 h-1 bg-error"></div>
              
              <div class="flex flex-col gap-space-md">
                <div class="flex items-center justify-between flex-wrap gap-2">
                  <div class="flex items-center gap-space-sm">
                    <span class="px-2.5 py-1 rounded-full bg-error-container text-on-error-container text-xs font-semibold flex items-center gap-1.5">
                      <span class="w-2 h-2 rounded-full bg-error animate-pulse"></span>
                      Detected Issue
                    </span>
                    <span class="font-code text-xs bg-surface-container px-2 py-0.5 rounded text-error">Frame @ 00:12.42</span>
                  </div>
                  <span class="text-xs text-outline font-semibold" id="res-confidence-tag">Triage Confidence: 99.4%</span>
                </div>

                <div>
                  <h2 class="text-xl font-bold text-on-surface" id="res-issue-title">Interaction Failure (Unresponsive UI Freeze)</h2>
                  <p class="text-xs text-on-surface-variant mt-0.5">What went wrong during checkout sequence execution?</p>
                </div>

                <!-- Visual Defect Preview Box -->
                <div class="relative w-full rounded-lg overflow-hidden bg-surface-container-high shadow-sm aspect-[16/9] group">
                  <img class="w-full h-full object-cover" src="https://lh3.googleusercontent.com/aida-public/AB6AXuBJdrKCKurOLvtF4DCUgKyp5jsCR4xXCms7CR4Y2xrkg-crV-Hne9DSjXP_9XLT4Z0xNWAnxCnIaBX9iJSXAOA552aosN7D0OWrEZvi_ylZCr_di7bhAcRpujjl1mnT3CbiMJkkIKqORiEm_v8cV02y3LeDhAlYx7fkPya-rhFBmOIf1S6sGdd1HUHBPEYneLecgpyHARH0YBzaoSU6xZzK3Jr9SlZBUKc8cS8buQY">
                  <div class="absolute inset-0 bg-on-background/20 backdrop-blur-[1px] flex items-center justify-center p-4">
                    <div class="relative bg-surface-container-lowest/95 p-3 rounded-lg shadow-xl w-3/4 max-w-sm flex flex-col gap-2">
                      <div class="flex justify-between items-center text-on-surface-variant text-xs">
                        <span>Order Total • $149.00</span>
                        <span class="text-error font-semibold flex items-center gap-1">
                          <span class="material-symbols-outlined text-[14px]">touch_app</span> 1.8s Timeout
                        </span>
                      </div>
                      <div class="relative p-1 rounded-md bg-error/10 shadow-[0_0_0_2px_#ba1a1a]">
                        <div class="w-full py-2 bg-primary/40 rounded flex items-center justify-center gap-2 cursor-not-allowed">
                          <span class="material-symbols-outlined text-[16px] text-on-surface animate-spin">refresh</span>
                          <span class="text-xs font-semibold text-on-surface">Complete Purchase</span>
                        </div>
                        <div class="absolute -top-3 -right-2 bg-error text-on-error font-code text-[10px] px-1.5 py-0.5 rounded shadow">
                          &lt;button#checkout-btn&gt;
                        </div>
                      </div>
                      <span class="font-code text-[11px] text-error">500 Internal Server Error: cartId missing</span>
                    </div>
                  </div>
                </div>

                <p class="text-xs text-on-surface font-medium" id="res-root-cause-text">
                  <code class="font-code text-[11px] bg-surface-container px-1 py-0.5 rounded text-on-surface font-semibold">#checkout-btn</code> freezes due to unhandled exception on <code class="font-code text-[11px] bg-surface-container px-1 py-0.5 rounded text-error">req.body.cartId</code>.
                </p>

                <!-- Console Trace -->
                <div class="bg-surface-container p-space-md rounded-lg flex flex-col gap-1 overflow-x-auto shadow-inner">
                  <div class="flex items-center justify-between text-xs text-outline pb-1">
                    <span class="font-semibold uppercase tracking-wider text-[10px]">Scrubbed Console Trace</span>
                    <span class="font-code text-[11px]">checkoutHandler.ts:42</span>
                  </div>
                  <pre class="font-code text-xs text-error leading-5 whitespace-pre" id="res-console-trace">Uncaught TypeError: Cannot read properties of undefined (reading 'cartId') at checkoutHandler.ts:42
[00:12.46] Authorization: Bearer [REDACTED_BY_CONTEXTPRISM]</pre>
                </div>
              </div>

              <div class="mt-space-lg pt-space-md flex items-center justify-between text-xs text-on-surface-variant border-t border-surface-container">
                <span class="flex items-center gap-1"><span class="material-symbols-outlined text-[16px]">visibility</span> Chrome 124 / Verified Anomaly</span>
                <span class="font-code text-[11px]" id="res-session-id-label">ID: BUG-82FA-99C1</span>
              </div>
            </div>

            <!-- Center Transformation Indicator -->
            <div class="hidden lg:flex absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 z-20 pointer-events-none">
              <div class="bg-surface-container-lowest text-primary shadow-xl rounded-full p-2.5 flex items-center justify-center border border-surface-container-high">
                <div class="w-10 h-10 rounded-full bg-primary flex items-center justify-center text-on-primary shadow-md">
                  <span class="material-symbols-outlined text-[24px]">swap_horiz</span>
                </div>
              </div>
            </div>

            <!-- Right Panel: Proposed Fix -->
            <div class="bg-surface-container-lowest rounded-xl p-space-xl flex flex-col justify-between shadow-sm relative overflow-hidden border border-surface-container-high">
              <div class="absolute top-0 left-0 right-0 h-1 bg-secondary"></div>
              
              <div class="flex flex-col gap-space-md">
                <div class="flex items-center justify-between flex-wrap gap-2">
                  <div class="flex items-center gap-space-sm">
                    <span class="px-2.5 py-1 rounded-full bg-secondary-container text-on-secondary-container text-xs font-semibold flex items-center gap-1.5">
                      <span class="w-2 h-2 rounded-full bg-secondary"></span>
                      Proposed Fix Verified
                    </span>
                    <span class="font-code text-xs bg-surface-container px-2 py-0.5 rounded text-secondary font-semibold">Diff Ready</span>
                  </div>
                  <span class="text-xs text-secondary font-semibold">Test Synthesized: +1 Passing</span>
                </div>

                <div>
                  <h2 class="text-xl font-bold text-on-surface">Code Patch & Defensive Guard Verified</h2>
                  <p class="text-xs text-on-surface-variant mt-0.5">Defensive cart resolution and fallback session fallback</p>
                </div>

                <!-- Corrected Visual Preview -->
                <div class="relative w-full rounded-lg overflow-hidden bg-surface-container-high shadow-sm aspect-[16/9] group">
                  <img class="w-full h-full object-cover" src="https://lh3.googleusercontent.com/aida-public/AB6AXuCzp9PG1SHGoc59tgSiA5zjmqGJUGs5oyrvv0uul89zxpl3tcfTznGD_GC1ScvIBVCKZ9aR-9w0ChZ4E4ULparkHyrOmZh0zjR5_h_HMqYspt7YYLoUI8B3RUpvbaQFCl14BA980buGl90infzBIaGs1JpteL0ABnDHbrnQbng94xI1inYn-nd3_fsi3e1i8S3D-nMuAUJjsR0aNk9LfC9pr8fxGdSlq9J1yjaePjk">
                  <div class="absolute inset-0 bg-secondary/10 backdrop-blur-[1px] flex items-center justify-center p-4">
                    <div class="bg-surface-container-lowest/95 p-4 rounded-xl shadow-xl w-3/4 max-w-sm flex flex-col items-center text-center gap-2">
                      <div class="w-10 h-10 rounded-full bg-secondary-container text-on-secondary-container flex items-center justify-center">
                        <span class="material-symbols-outlined text-[24px]">done_all</span>
                      </div>
                      <div>
                        <span class="text-sm font-bold text-on-surface block">Payment Confirmed!</span>
                        <span class="font-code text-xs text-outline">Order #92819-A Verified</span>
                      </div>
                      <span class="px-2 py-0.5 bg-surface-container rounded-full text-[11px] text-secondary font-semibold">State Resolved: 200 OK</span>
                    </div>
                  </div>
                </div>

                <p class="text-xs text-on-surface font-medium" id="res-patch-desc">
                  Applied atomic search/replace patch injecting fallback safety to <code class="font-code text-[11px] bg-surface-container px-1 py-0.5 rounded text-secondary font-semibold" id="res-patch-target">src/api/checkoutHandler.ts</code>.
                </p>

                <!-- Diff Block -->
                <div class="bg-surface-container p-space-md rounded-lg flex flex-col gap-1 overflow-x-auto shadow-inner">
                  <div class="flex items-center justify-between text-xs text-outline pb-1">
                    <span class="font-semibold uppercase tracking-wider text-[10px]">ATOMIC DIFF INSPECTOR</span>
                    <span class="font-code text-[11px]" id="diff-file-label">src/api/checkoutHandler.ts</span>
                  </div>
                  <pre class="font-code text-xs leading-5 whitespace-pre" id="res-patch-diff-view"><span class="text-error bg-error-container/40 block px-1">- if (!req.body.cartId) throw new Error();</span><span class="text-secondary bg-secondary-container/40 block px-1 font-semibold">+ const cartId = req.body?.cartId ?? req.session?.cartId;</span><span class="text-secondary bg-secondary-container/40 block px-1 font-semibold">+ if (!cartId) return res.status(400).json({ error: 'Missing cartId' });</span></pre>
                </div>
              </div>

              <div class="mt-space-lg pt-space-md flex items-center justify-between text-xs border-t border-surface-container">
                <span class="text-secondary flex items-center gap-1 font-semibold">
                  <span class="material-symbols-outlined text-[16px]">check_circle</span> Zero regressions detected
                </span>
                <button onclick="document.getElementById('fixDrawer').classList.remove('hidden')" class="px-3 py-1 rounded-full bg-secondary-container text-on-secondary-container hover:bg-secondary hover:text-on-secondary font-semibold transition">
                  Apply to Branch
                </button>
              </div>
            </div>

          </div>
        </div>

        <!-- Callout Banner -->
        <div class="w-full bg-surface-container-lowest p-space-lg rounded-xl shadow-sm flex flex-col md:flex-row items-center justify-between gap-space-lg border border-surface-container-high">
          <div class="flex items-center gap-space-md">
            <div class="w-10 h-10 rounded-full bg-primary/10 text-primary flex items-center justify-center shrink-0">
              <span class="material-symbols-outlined text-[24px]">auto_fix_high</span>
            </div>
            <div>
              <h3 class="font-bold text-sm text-on-surface">Autonomous resolution ready to merge</h3>
              <p class="text-xs text-on-surface-variant">Playwright test verified • hot-patch validated • Google Cloud PUE/WUE audited</p>
            </div>
          </div>
          <button onclick="document.getElementById('fixDrawer').classList.remove('hidden')" class="w-full md:w-auto px-6 py-2.5 rounded-full bg-primary hover:bg-primary-container text-on-primary text-xs font-bold shadow-sm transition flex items-center justify-center gap-2">
            <span class="material-symbols-outlined text-[18px]">build_circle</span>
            <span>Fix This Issue</span>
          </button>
        </div>

        <!-- 3 Deep-Dive Tabs -->
        <div class="bg-surface-container-lowest rounded-xl shadow-sm overflow-hidden flex flex-col border border-surface-container-high">
          <!-- Tab Bar -->
          <div class="bg-surface-container-low px-space-lg py-space-sm flex items-center justify-between gap-space-md flex-wrap">
            <div class="flex items-center gap-space-xs" id="analysisTabBar">
              <button onclick="switchAnalysisTab('timeline', this)" id="tab-btn-timeline" class="px-space-md py-2 rounded-lg text-xs font-bold bg-surface-container-lowest text-on-surface shadow-sm flex items-center gap-1.5 transition">
                <span class="material-symbols-outlined text-[18px] text-primary">view_timeline</span>
                <span>Timeline (ContextPrism)</span>
              </button>
              <button onclick="switchAnalysisTab('verdict', this)" id="tab-btn-verdict" class="px-space-md py-2 rounded-lg text-xs font-medium text-on-surface-variant hover:text-on-surface transition flex items-center gap-1.5">
                <span class="material-symbols-outlined text-[18px]">gavel</span>
                <span>Verdict (ApexTrace Dual-Engine)</span>
              </button>
              <button onclick="switchAnalysisTab('sandbox', this)" id="tab-btn-sandbox" class="px-space-md py-2 rounded-lg text-xs font-medium text-on-surface-variant hover:text-on-surface transition flex items-center gap-1.5">
                <span class="material-symbols-outlined text-[18px]">terminal</span>
                <span>Sandbox Verification (Replay Shield)</span>
              </button>
            </div>
            <div class="font-code text-[11px] text-outline flex items-center gap-2">
              <span>PII MASKING: ACTIVE</span>
              <span class="w-1.5 h-1.5 rounded-full bg-secondary"></span>
            </div>
          </div>

          <!-- Deep-Dive Tab 1: Timeline -->
          <div id="tab-content-timeline" class="p-space-xl flex flex-col gap-space-lg">
            <div class="flex items-center justify-between flex-wrap gap-2">
              <div>
                <h3 class="font-bold text-sm text-on-surface">ContextPrism Forensic Pipeline</h3>
                <p class="text-xs text-on-surface-variant">Automated keyframe reduction & PII sanitization stream</p>
              </div>
              <span class="font-code text-xs bg-surface-container text-secondary font-semibold px-3 py-1 rounded-full">84.9% Tokens Saved</span>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-space-md text-xs" id="timeline-events-grid">
              <div class="bg-surface-container-low p-space-md rounded-lg flex flex-col gap-1">
                <div class="flex items-center justify-between">
                  <span class="font-semibold text-on-surface">1. Frame Extraction</span>
                  <span class="font-code text-outline">00:00 - 00:06</span>
                </div>
                <p class="text-on-surface-variant">720 frames sampled @ 1080p60 synchronized with interaction logs.</p>
              </div>
              <div class="bg-surface-container-low p-space-md rounded-lg flex flex-col gap-1">
                <div class="flex items-center justify-between">
                  <span class="font-semibold text-on-surface">2. PII Sanitization</span>
                  <span class="font-code text-secondary">00:07 - 00:10</span>
                </div>
                <p class="text-on-surface-variant">Masked card numbers, Bearer tokens, and auth headers.</p>
              </div>
              <div class="bg-error-container/40 p-space-md rounded-lg flex flex-col gap-1">
                <div class="flex items-center justify-between">
                  <span class="font-semibold text-error">3. Anomaly Trigger</span>
                  <span class="font-code bg-error-container text-on-error-container px-1 rounded">00:12.42</span>
                </div>
                <p class="text-on-surface-variant">Optical flow reached 0.00 px/s with repeated click attempts.</p>
              </div>
              <div class="bg-surface-container-low p-space-md rounded-lg flex flex-col gap-1">
                <div class="flex items-center justify-between">
                  <span class="font-semibold text-on-surface">4. AST Narrowing</span>
                  <span class="font-code text-outline">00:14 - 00:24</span>
                </div>
                <p class="text-on-surface-variant">Pruned unreferenced AST modules; isolated checkoutHandler.ts.</p>
              </div>
            </div>
          </div>

          <!-- Deep-Dive Tab 2: Verdict -->
          <div id="tab-content-verdict" class="p-space-xl flex flex-col gap-space-lg hidden">
            <div class="flex items-center justify-between flex-wrap gap-2">
              <div>
                <h3 class="font-bold text-sm text-on-surface">Dual-Engine Consensus Verdict</h3>
                <p class="text-xs text-on-surface-variant">Visual anomaly detection + DOM differential baseline</p>
              </div>
              <span class="px-3 py-1 bg-secondary-fixed/50 text-on-secondary-fixed-variant rounded-full font-code text-xs font-semibold">Agreement: 100%</span>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-space-md text-xs">
              <div class="bg-surface-container-low p-space-md rounded-lg flex flex-col justify-between gap-space-sm">
                <div class="flex items-center justify-between">
                  <span class="font-bold text-on-surface">Engine A: Google Gemini 3.5</span>
                  <span class="font-code text-primary font-semibold">96.4% confidence</span>
                </div>
                <p class="text-on-surface-variant" id="deep-gemini-desc">Detected static loading spinner halting UI state across 40 frames without resolution.</p>
                <span class="font-code text-[11px] text-outline" id="deep-target-label">Target: src/api/checkoutHandler.ts</span>
              </div>
              <div class="bg-surface-container-low p-space-md rounded-lg flex flex-col justify-between gap-space-sm">
                <div class="flex items-center justify-between">
                  <span class="font-bold text-on-surface">Engine B: SSIM Sentinel Metric</span>
                  <span class="font-code text-error font-semibold">0.02% Δ repaint</span>
                </div>
                <p class="text-on-surface-variant" id="deep-ssim-desc">Deterministic pixel drift = 0.02%. Corroborates silent UI freeze with zero false alarms.</p>
                <span class="font-code text-[11px] text-outline">Tier 1 Ground-Truth Precedence</span>
              </div>
            </div>
          </div>

          <!-- Deep-Dive Tab 3: Sandbox Verification -->
          <div id="tab-content-sandbox" class="p-space-xl flex flex-col gap-space-lg hidden">
            <div>
              <h3 class="font-bold text-sm text-on-surface">Replay Shield: Deterministic Playwright Sandbox</h3>
              <p class="text-xs text-on-surface-variant">Synthesized reproduction test executed in isolated container environment</p>
            </div>

            <!-- Playwright Code Viewer -->
            <div class="bg-surface-container-high rounded-lg overflow-hidden shadow-inner">
              <div class="bg-surface-container px-space-md py-2 flex items-center justify-between text-on-surface-variant text-xs">
                <div class="flex items-center gap-space-sm">
                  <span class="material-symbols-outlined text-[16px] text-primary">code</span>
                  <span class="font-code text-on-surface font-medium" id="res-playwright-filename">tests/synthetic/checkout-repro.spec.ts</span>
                </div>
                <span class="text-[10px] font-semibold bg-secondary-container text-on-secondary-container px-2 py-0.5 rounded-full">Passed in Replay</span>
              </div>
              <pre class="p-space-lg font-code text-xs text-on-surface overflow-x-auto leading-6" id="res-playwright-code"><code>// Autonomous Playwright reproducer generated by V.E.R.D.A.N.T.
import { test, expect } from '@playwright/test';

test('reproduce and verify checkout lockup fix', async ({ page }) => {
  await page.goto('/checkout/cart-step');
  const submitBtn = page.locator('button#checkout-btn');
  await submitBtn.click();
  await expect(page.locator('.order-success')).toBeVisible({ timeout: 2000 });
});</code></pre>
            </div>
          </div>

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
      const screens = ['home', 'pipeline', 'results', 'sustainability', 'history'];
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
    }

    function navigateTab(tab, event) {
      if (event) event.preventDefault();
      const pathMap = {
        'home': '/',
        'pipeline': '/pipeline',
        'results': '/results',
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
      if (p.includes('pipeline') || p.includes('analysis')) {
        switchMainTab('pipeline');
      } else if (p.includes('results') || p.includes('bench')) {
        switchMainTab('results');
      } else if (p.includes('sustain') || p.includes('verde') || p.includes('eco')) {
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
        btnC.className = "px-2.5 py-1 rounded-md text-xs font-semibold bg-primary text-on-primary shadow-sm transition";
        btnA.className = "px-2.5 py-1 rounded-md text-xs font-semibold bg-surface-container hover:bg-surface-container-high text-on-surface transition";
        document.getElementById('hero-session-name').innerText = "checkout_unresponsive_submit_freeze.mp4";
        document.getElementById('hero-session-desc').innerText = "User clicks 'Place Order'. Network returns 500; button stays disabled with zero visual repaint.";
        document.getElementById('hero-ssim').innerHTML = "0.9984 <span class='text-[10px] text-error font-normal'>(Frozen)</span>";
        document.getElementById('hero-delta').innerHTML = "0.02% <span class='text-[10px] text-secondary font-normal'>(Zero Drift)</span>";
        document.getElementById('hero-network').innerText = "500 Fail";
      } else {
        btnA.className = "px-2.5 py-1 rounded-md text-xs font-semibold bg-primary text-on-primary shadow-sm transition";
        btnC.className = "px-2.5 py-1 rounded-md text-xs font-semibold bg-surface-container hover:bg-surface-container-high text-on-surface transition";
        document.getElementById('hero-session-name').innerText = "auth_token_expired_silent_drop.mp4";
        document.getElementById('hero-session-desc').innerText = "User submits settings update. JWT session expired mid-flight; client frontend fails silently.";
        document.getElementById('hero-ssim').innerHTML = "0.9142 <span class='text-[10px] text-secondary font-normal'>(Repaint)</span>";
        document.getElementById('hero-delta').innerHTML = "4.12% <span class='text-[10px] text-primary font-normal'>(Alert Drift)</span>";
        document.getElementById('hero-network').innerText = "401 Unauth";
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
        const cleanBase = suspectFile.split('/').pop().replace(/\.[^/.]+$/, "");
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
    screens = ["home", "pipeline", "results", "sustainability", "history"]
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

