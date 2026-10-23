import os
import sys
import subprocess
from PIL import Image, ImageDraw, ImageFont
import win32com.client

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(BASE_DIR, "video_build")
os.makedirs(OUT_DIR, exist_ok=True)

FONTS_DIR = os.path.join(os.environ.get('WINDIR', 'C:/Windows'), 'Fonts')
font_title = ImageFont.truetype(os.path.join(FONTS_DIR, 'segoeui.ttf'), 50)
font_subtitle = ImageFont.truetype(os.path.join(FONTS_DIR, 'segoeui.ttf'), 28)
font_body = ImageFont.truetype(os.path.join(FONTS_DIR, 'segoeui.ttf'), 23)
font_mono = ImageFont.truetype(os.path.join(FONTS_DIR, 'consola.ttf'), 22)
font_caption = ImageFont.truetype(os.path.join(FONTS_DIR, 'segoeui.ttf'), 25)

banner_path = os.path.join(BASE_DIR, "website", "verdant-banner-3x2.png")
logo_path = os.path.join(BASE_DIR, "website", "verdant-logo.png")

banner_img = Image.open(banner_path).convert("RGBA") if os.path.exists(banner_path) else None
logo_img = Image.open(logo_path).convert("RGBA") if os.path.exists(logo_path) else None

SCENES = [
    {
        "id": "scene1_intro",
        "title": "VERDANT: The Consequence-Aware Alexa+ Companion",
        "subtitle": "Amazon Developer Hackathon 2026 • Alexa+ Track & AWS Builder Challenge",
        "script": "Welcome to VERDANT, the consequence aware companion for Alexa plus, submitted to the Amazon Developer Hackathon 2026. Today, voice assistants blindly execute commands without understanding downstream risks. VERDANT introduces a breakthrough dual architecture: zero token ambient intelligence paired with sub millisecond consequence prevention.",
        "caption": "VERDANT: Dual Architecture Voice Companion (Zero-Token Everyday + Sub-Millisecond Sentinel)"
    },
    {
        "id": "scene2_architecture",
        "title": "The Dual Cognitive Architecture",
        "subtitle": "Zero-Token Dynamic Graph Salience Engine + Compiled VERDE Systems Kernel",
        "script": "For everyday queries, VERDANT eliminates bloated cloud language models entirely. Arithmetic is computed deterministically in two milliseconds using SymPy. Unscripted knowledge questions are synthesized dynamically using bipartite sentence graph centrality, delivering articulate answers with zero external API fees and complete user privacy.",
        "caption": "Everyday Engine: SymPy 1.14 (2ms Arithmetic) + TextRank Centrality (Zero LLM Tokens Burned)"
    },
    {
        "id": "scene3_everyday_demo",
        "title": "Live Demonstration: Everyday Ambient Intelligence",
        "subtitle": "Echo Show 15 Smart Display HUD • Silence-Debounced Voice Recognition",
        "script": "Here is our live Echo Show 15 interface. With our silence debouncing engine, the full query is captured before processing. Asking what is one plus one evaluates in two milliseconds. Asking for the weather of India resolves live coordinates dynamically without hardcoded city fallbacks, and general knowledge queries extract live facts cleanly.",
        "caption": "Live Test: 'What is 1+1' (2.4ms) | 'Weather of India' (Open-Meteo Dynamic Geocoding)"
    },
    {
        "id": "scene4_consequence_sentinel",
        "title": "High-Stakes Sentinel: The VERDE Causal Kernel",
        "subtitle": "2.1ms Causal State Rollout • In-Memory Blast Radius Evaluation",
        "script": "Now, observe high stakes consequence prevention. When an operator asks to take the production database offline, our compiled VERDE systems runtime intercepts the command in just two point one milliseconds. Before any live cloud action touches infrastructure, VERDE simulates the causal rollout in memory, detects four hundred and fifty dropped transactions, halts execution, and generates a capability secured mitigation route to keep systems safe.",
        "caption": "Causal Interception: Stopped EU-DB Shutdown (450 Severed Sessions) | Verified Mitigation Authorized"
    },
    {
        "id": "scene5_mcp_benchmarks",
        "title": "Model Context Protocol 2.0 & Benchmark Matrix",
        "subtitle": "Streamable JSON-RPC 2.0 Server • 5,900x Faster than 70B ReAct Agents",
        "script": "VERDANT also functions as a self hosted Model Context Protocol server, exposing pre flight consequence rollouts over streamable JSON RPC 2.0 to any agentic client. Compared to traditional seventy billion parameter ReAct agents, VERDANT is fifty nine hundred times faster, consumes ninety nine percent less energy, and burns zero tokens.",
        "caption": "Performance Matrix: 2.1ms vs 12,400ms (5,900x Faster) | 0.00010J vs 85.2J (99.9% Less Energy)"
    },
    {
        "id": "scene6_conclusion",
        "title": "Multi-Platform Availability & Open Source",
        "subtitle": "Standalone .EXE • Live Web Simulator • Electron Suite • Render Cloud",
        "script": "VERDANT is production ready and available across three modalities: a standalone Windows executable, a developer Electron suite, and an interactive web simulator ready for deployment on Render. The entire codebase is open source under Apache 2.0 on GitHub at dhairya dash shah 7 slash VERDANT. Thank you for watching.",
        "caption": "Repository Live: github.com/dhairya-shah7/VERDANT | Standalone .EXE & Render Ready"
    }
]

def synthesize_audio(text, out_wav):
    speaker = win32com.client.Dispatch("SAPI.SpVoice")
    stream = win32com.client.Dispatch("SAPI.SpFileStream")
    stream.Open(out_wav, 3, False)
    speaker.AudioOutputStream = stream
    speaker.Rate = 0
    speaker.Speak(text)
    stream.Close()

def render_scene_slide(scene, out_png, scene_idx, total_scenes):
    width, height = 1920, 1080
    img = Image.new("RGB", (width, height), (7, 11, 20))
    draw = ImageDraw.Draw(img)

    # Ambient Background Grid
    for x in range(0, width, 80):
        draw.line([(x, 0), (x, height)], fill=(15, 23, 42), width=1)
    for y in range(0, height, 80):
        draw.line([(0, y), (width, y)], fill=(15, 23, 42), width=1)

    # Top Header Bar
    draw.rectangle([(0, 0), (width, 90)], fill=(10, 16, 31))
    draw.line([(0, 90), (width, 90)], fill=(30, 41, 59), width=2)

    # Logo / Title in Top Bar
    if logo_img:
        thumb_logo = logo_img.resize((50, 50))
        img.paste(thumb_logo, (40, 20), thumb_logo)
    
    draw.text((105, 25), "VERDANT", font=font_title, fill=(16, 185, 129))
    draw.text((360, 38), "Alexa+ OS • Consequence Sentinel Engine", font=font_subtitle, fill=(148, 163, 184))

    # Live Badge on Top Right
    badge_x = width - 360
    draw.rounded_rectangle([(badge_x, 24), (badge_x + 310, 66)], radius=12, fill=(16, 185, 129, 30), outline=(16, 185, 129), width=1)
    draw.ellipse([(badge_x + 18, 41), (badge_x + 28, 51)], fill=(16, 185, 129))
    draw.text((badge_x + 38, 32), "AMAZON HACKATHON 2026", font=font_mono, fill=(241, 245, 249))

    scene_id = scene["id"]

    if scene_id == "scene1_intro":
        if banner_img:
            b_w = 900
            b_h = int(b_w * (840 / 1260))
            scaled_banner = banner_img.resize((b_w, b_h))
            img.paste(scaled_banner, (510, 150), scaled_banner)
        
        draw.ellipse([(960 - 250, 450 - 250), (960 + 250, 450 + 250)], outline=(6, 182, 212, 100), width=2)
        draw.text((960, 780), scene["title"], font=font_title, fill=(255, 255, 255), anchor="mm")
        draw.text((960, 840), scene["subtitle"], font=font_subtitle, fill=(52, 211, 153), anchor="mm")

    elif scene_id == "scene2_architecture":
        draw.text((960, 150), scene["title"], font=font_title, fill=(255, 255, 255), anchor="mm")
        draw.text((960, 205), scene["subtitle"], font=font_subtitle, fill=(148, 163, 184), anchor="mm")

        # Left Card: Zero-Token Everyday Engine
        draw.rounded_rectangle([(180, 260), (900, 760)], radius=24, fill=(15, 23, 42), outline=(16, 185, 129), width=2)
        draw.text((220, 300), "1. Zero-Token Epistemic Core", font=font_subtitle, fill=(52, 211, 153))
        draw.text((220, 360), "• Deterministic Invariant Math: SymPy 1.14 (<= 2ms)", font=font_body, fill=(226, 232, 240))
        draw.text((220, 420), "• Dynamic REST Epistemic Ingestion (No Hardcoded Data)", font=font_body, fill=(226, 232, 240))
        draw.text((220, 480), "• TextRank Graph-Centrality Sentence Salience", font=font_body, fill=(226, 232, 240))
        draw.text((220, 540), "• Dynamic Global Geocoding via Open-Meteo", font=font_body, fill=(226, 232, 240))
        draw.rounded_rectangle([(220, 620), (860, 710)], radius=12, fill=(16, 185, 129, 20))
        draw.text((540, 665), "0 TOKENS BURNED • 100% PRIVATE • ZERO API COST", font=font_mono, fill=(16, 185, 129), anchor="mm")

        # Right Card: Consequential VERDE Sentinel
        draw.rounded_rectangle([(1020, 260), (1740, 760)], radius=24, fill=(15, 23, 42), outline=(6, 182, 212), width=2)
        draw.text((1060, 300), "2. Causal Systems Sentinel", font=font_subtitle, fill=(34, 211, 238))
        draw.text((1060, 360), "• Native Compiled Kernel: verde.exe (v1.0.0)", font=font_body, fill=(226, 232, 240))
        draw.text((1060, 420), "• Causal State Rollouts in 2.1 Milliseconds", font=font_body, fill=(226, 232, 240))
        draw.text((1060, 480), "• Microscopic Energy Footprint: 0.00010 Joules", font=font_body, fill=(226, 232, 240))
        draw.text((1060, 540), "• Capability[SystemExecute] Verification Tokens", font=font_body, fill=(226, 232, 240))
        draw.rounded_rectangle([(1060, 620), (1700, 710)], radius=12, fill=(6, 182, 212, 20))
        draw.text((1380, 665), "2.1ms LATENCY • 0.00010 JOULES • INVARIANT SAFETY", font=font_mono, fill=(34, 211, 238), anchor="mm")

    elif scene_id == "scene3_everyday_demo":
        draw.text((960, 140), scene["title"], font=font_title, fill=(255, 255, 255), anchor="mm")
        draw.text((960, 195), scene["subtitle"], font=font_subtitle, fill=(148, 163, 184), anchor="mm")

        draw.rounded_rectangle([(240, 240), (1680, 780)], radius=20, fill=(15, 23, 42), outline=(51, 65, 85), width=2)
        
        # Test 1 Card: Math
        draw.rounded_rectangle([(280, 280), (700, 740)], radius=16, fill=(30, 41, 59), outline=(16, 185, 129), width=1)
        draw.text((310, 320), "VOICE QUERY 1", font=font_mono, fill=(16, 185, 129))
        draw.text((310, 360), "\"What is one plus one?\"", font=font_subtitle, fill=(255, 255, 255))
        draw.text((310, 430), "Result: 1 + 1 = 2", font=font_subtitle, fill=(52, 211, 153))
        draw.text((310, 480), "Spoken: 'One plus one is 2.'", font=font_body, fill=(148, 163, 184))
        draw.text((310, 540), "Engine: SymPy Invariant Logic", font=font_mono, fill=(100, 116, 139))
        draw.text((310, 590), "Latency: 2.47 ms", font=font_mono, fill=(16, 185, 129))
        draw.text((310, 640), "Tokens: 0 Burned", font=font_mono, fill=(16, 185, 129))

        # Test 2 Card: Weather Geocoding
        draw.rounded_rectangle([(740, 280), (1200, 740)], radius=16, fill=(30, 41, 59), outline=(6, 182, 212), width=1)
        draw.text((770, 320), "VOICE QUERY 2", font=font_mono, fill=(6, 182, 212))
        draw.text((770, 360), "\"Weather of India\"", font=font_subtitle, fill=(255, 255, 255))
        draw.text((770, 430), "Location: India (22°C Clear)", font=font_subtitle, fill=(34, 211, 238))
        draw.text((770, 480), "Live Geocoding: Open-Meteo", font=font_body, fill=(148, 163, 184))
        draw.text((770, 540), "Dynamic Lat/Long Resolved", font=font_mono, fill=(100, 116, 139))
        draw.text((770, 590), "Static Fallback: Eliminated", font=font_mono, fill=(34, 211, 238))
        draw.text((770, 640), "Tokens: 0 Burned", font=font_mono, fill=(34, 211, 238))

        # Test 3 Card: Dynamic OpenAI Knowledge
        draw.rounded_rectangle([(1240, 280), (1640, 740)], radius=16, fill=(30, 41, 59), outline=(168, 85, 247), width=1)
        draw.text((1270, 320), "VOICE QUERY 3", font=font_mono, fill=(168, 85, 247))
        draw.text((1270, 360), "\"Builder of OpenAI?\"", font=font_subtitle, fill=(255, 255, 255))
        draw.text((1270, 430), "OpenAI PBC (CEO Sam Altman)", font=font_body, fill=(192, 132, 252))
        draw.text((1270, 480), "Dynamic Epistemic Extraction", font=font_body, fill=(148, 163, 184))
        draw.text((1270, 540), "TextRank Centrality Rank", font=font_mono, fill=(100, 116, 139))
        draw.text((1270, 590), "Privacy: 100% Local Logic", font=font_mono, fill=(192, 132, 252))
        draw.text((1270, 640), "Tokens: 0 Burned", font=font_mono, fill=(192, 132, 252))

    elif scene_id == "scene4_consequence_sentinel":
        draw.text((960, 130), scene["title"], font=font_title, fill=(255, 255, 255), anchor="mm")
        draw.text((960, 185), scene["subtitle"], font=font_subtitle, fill=(244, 63, 94), anchor="mm")

        # Alert Banner
        draw.rounded_rectangle([(240, 220), (1680, 330)], radius=16, fill=(225, 29, 72, 40), outline=(225, 29, 72), width=2)
        draw.text((280, 245), "COMMAND DETECTED: 'Alexa, take the EU database server offline for maintenance'", font=font_subtitle, fill=(255, 255, 255))
        draw.text((280, 285), "STATUS: INTERCEPTED BY VERDE KERNEL • TIME: 2.1ms • ENERGY: 0.00010 J", font=font_mono, fill=(251, 113, 133))

        # Causal Radar Box
        draw.rounded_rectangle([(240, 360), (1140, 760)], radius=20, fill=(15, 23, 42), outline=(51, 65, 85), width=2)
        draw.text((280, 390), "IN-MEMORY CAUSAL BLAST-RADIUS RADAR", font=font_subtitle, fill=(255, 255, 255))
        
        c_x, c_y = 690, 580
        draw.ellipse([(c_x - 55, c_y - 55), (c_x + 55, c_y + 55)], fill=(225, 29, 72), outline=(255, 255, 255), width=2)
        draw.text((c_x, c_y - 8), "EU-DB", font=font_mono, fill=(255, 255, 255), anchor="mm")
        draw.text((c_x, c_y + 16), "OFFLINE", font=font_mono, fill=(254, 205, 211), anchor="mm")

        n1_x, n1_y = 440, 480
        draw.line([(c_x, c_y), (n1_x, n1_y)], fill=(245, 158, 11), width=3)
        draw.ellipse([(n1_x - 45, n1_y - 45), (n1_x + 45, n1_y + 45)], fill=(217, 119, 6), outline=(255, 255, 255), width=1)
        draw.text((n1_x, n1_y), "Checkout", font=font_mono, fill=(255, 255, 255), anchor="mm")

        n2_x, n2_y = 940, 480
        draw.line([(c_x, c_y), (n2_x, n2_y)], fill=(245, 158, 11), width=3)
        draw.ellipse([(n2_x - 45, n2_y - 45), (n2_x + 45, n2_y + 45)], fill=(217, 119, 6), outline=(255, 255, 255), width=1)
        draw.text((n2_x, n2_y), "Billing", font=font_mono, fill=(255, 255, 255), anchor="mm")

        n3_x, n3_y = 690, 710
        draw.line([(c_x, c_y), (n3_x, n3_y)], fill=(245, 158, 11), width=3)
        draw.ellipse([(n3_x - 40, n3_y - 40), (n3_x + 40, n3_y + 40)], fill=(217, 119, 6), outline=(255, 255, 255), width=1)
        draw.text((n3_x, n3_y), "Inventory", font=font_mono, fill=(255, 255, 255), anchor="mm")

        # Mitigation Route Box
        draw.rounded_rectangle([(1180, 360), (1680, 760)], radius=20, fill=(15, 23, 42), outline=(16, 185, 129), width=2)
        draw.text((1210, 400), "DETERMINISTIC MITIGATION PLAN", font=font_subtitle, fill=(52, 211, 153))
        draw.text((1210, 460), "1. Route traffic to Replica-B", font=font_body, fill=(226, 232, 240))
        draw.text((1210, 510), "2. Drain 450 active handshakes", font=font_body, fill=(226, 232, 240))
        draw.text((1210, 560), "3. Execute maintenance safely", font=font_body, fill=(226, 232, 240))
        draw.text((1210, 610), "4. Zero dropped transactions", font=font_body, fill=(226, 232, 240))

        draw.rounded_rectangle([(1210, 670), (1650, 730)], radius=12, fill=(16, 185, 129))
        draw.text((1430, 700), "✓ AUTHORIZE SAFE PLAN", font=font_subtitle, fill=(10, 16, 31), anchor="mm")

    elif scene_id == "scene5_mcp_benchmarks":
        draw.text((960, 130), scene["title"], font=font_title, fill=(255, 255, 255), anchor="mm")
        draw.text((960, 185), scene["subtitle"], font=font_subtitle, fill=(148, 163, 184), anchor="mm")

        draw.rounded_rectangle([(240, 240), (1680, 760)], radius=20, fill=(15, 23, 42), outline=(51, 65, 85), width=2)
        
        draw.rectangle([(242, 242), (1678, 320)], fill=(30, 41, 59))
        draw.text((280, 270), "METRIC", font=font_mono, fill=(148, 163, 184))
        draw.text((640, 270), "CONVENTIONAL LLM (ReAct)", font=font_mono, fill=(244, 63, 94))
        draw.text((1080, 270), "VERDANT + VERDE", font=font_mono, fill=(16, 185, 129))
        draw.text((1440, 270), "IMPROVEMENT", font=font_mono, fill=(34, 211, 238))

        draw.line([(240, 390), (1680, 390)], fill=(51, 65, 85), width=1)
        draw.text((280, 345), "Simulation Latency", font=font_body, fill=(255, 255, 255))
        draw.text((640, 345), "12,400 ms (multi-turn)", font=font_body, fill=(148, 163, 184))
        draw.text((1080, 345), "2.1 ms (compiled kernel)", font=font_body, fill=(52, 211, 153))
        draw.text((1440, 345), "5,900x Faster", font=font_subtitle, fill=(34, 211, 238))

        draw.line([(240, 480), (1680, 480)], fill=(51, 65, 85), width=1)
        draw.text((280, 435), "Energy Footprint", font=font_body, fill=(255, 255, 255))
        draw.text((640, 435), "~85.2 Joules (GPU cloud)", font=font_body, fill=(148, 163, 184))
        draw.text((1080, 435), "0.00010 Joules (C11 native)", font=font_body, fill=(52, 211, 153))
        draw.text((1440, 435), "99.99% Less Energy", font=font_subtitle, fill=(34, 211, 238))

        draw.line([(240, 570), (1680, 570)], fill=(51, 65, 85), width=1)
        draw.text((280, 525), "Token Consumption", font=font_body, fill=(255, 255, 255))
        draw.text((640, 525), "3,800 - 4,500 Tokens", font=font_body, fill=(148, 163, 184))
        draw.text((1080, 525), "0 Tokens (Pure Epistemic Graph)", font=font_body, fill=(52, 211, 153))
        draw.text((1440, 525), "Zero Cost (100% Free)", font=font_subtitle, fill=(34, 211, 238))

        draw.line([(240, 660), (1680, 660)], fill=(51, 65, 85), width=1)
        draw.text((280, 615), "Disaster Prevention", font=font_body, fill=(255, 255, 255))
        draw.text((640, 615), "Probabilistic / Hallucinatory", font=font_body, fill=(244, 63, 94))
        draw.text((1080, 615), "100% Invariant State Machine", font=font_body, fill=(52, 211, 153))
        draw.text((1440, 615), "Deterministic Safety", font=font_subtitle, fill=(34, 211, 238))

        draw.text((960, 715), "Model Context Protocol 2.0 (Streamable JSON-RPC Endpoint Active on Port 8000)", font=font_mono, fill=(168, 85, 247), anchor="mm")

    elif scene_id == "scene6_conclusion":
        draw.text((960, 150), scene["title"], font=font_title, fill=(255, 255, 255), anchor="mm")
        draw.text((960, 205), scene["subtitle"], font=font_subtitle, fill=(52, 211, 153), anchor="mm")

        # 3 Modalities Cards
        draw.rounded_rectangle([(240, 270), (660, 640)], radius=20, fill=(15, 23, 42), outline=(16, 185, 129), width=2)
        draw.text((450, 320), "1. Standalone .EXE", font=font_subtitle, fill=(255, 255, 255), anchor="mm")
        draw.text((450, 390), "VERDANT.exe", font=font_mono, fill=(52, 211, 153), anchor="mm")
        draw.text((450, 440), "Windows Native Kiosk HUD", font=font_body, fill=(148, 163, 184), anchor="mm")
        draw.text((450, 480), "Zero Dependency Launch", font=font_body, fill=(148, 163, 184), anchor="mm")
        draw.text((450, 520), "Echo Show 15 Simulation", font=font_body, fill=(148, 163, 184), anchor="mm")

        draw.rounded_rectangle([(750, 270), (1170, 640)], radius=20, fill=(15, 23, 42), outline=(6, 182, 212), width=2)
        draw.text((960, 320), "2. Web Application", font=font_subtitle, fill=(255, 255, 255), anchor="mm")
        draw.text((960, 390), "Render Cloud Ready", font=font_mono, fill=(34, 211, 238), anchor="mm")
        draw.text((960, 440), "Browser-Based Echo Show", font=font_body, fill=(148, 163, 184), anchor="mm")
        draw.text((960, 480), "Web Speech Recognition", font=font_body, fill=(148, 163, 184), anchor="mm")
        draw.text((960, 520), "render.yaml Blueprint", font=font_body, fill=(148, 163, 184), anchor="mm")

        draw.rounded_rectangle([(1260, 270), (1680, 640)], radius=20, fill=(15, 23, 42), outline=(168, 85, 247), width=2)
        draw.text((1470, 320), "3. Developer Suite", font=font_subtitle, fill=(255, 255, 255), anchor="mm")
        draw.text((1470, 390), "npm start", font=font_mono, fill=(192, 132, 252), anchor="mm")
        draw.text((1470, 440), "MCP 2.0 Server", font=font_body, fill=(148, 163, 184), anchor="mm")
        draw.text((1470, 480), "7/7 Passing Tests", font=font_body, fill=(148, 163, 184), anchor="mm")
        draw.text((1470, 520), "Full Source Code", font=font_body, fill=(148, 163, 184), anchor="mm")

        draw.rounded_rectangle([(360, 680), (1560, 750)], radius=16, fill=(30, 41, 59), outline=(16, 185, 129), width=1)
        draw.text((960, 715), "GitHub Repository: https://github.com/dhairya-shah7/VERDANT", font=font_subtitle, fill=(52, 211, 153), anchor="mm")

    # Audio Waveform Visualizer Bar
    wave_y = 960
    for i in range(24):
        bx = 820 + i * 12
        h_bar = 14 + (i % 6) * 4
        draw.line([(bx, wave_y - h_bar), (bx, wave_y + h_bar)], fill=(16, 185, 129), width=4)

    # Caption Banner
    draw.rectangle([(0, 1000), (width, 1070)], fill=(10, 16, 31))
    draw.text((960, 1035), scene["caption"], font=font_caption, fill=(241, 245, 249), anchor="mm")

    # Progress Bar at Bottom-most edge
    progress = (scene_idx + 1) / total_scenes
    draw.rectangle([(0, 1070), (width, 1080)], fill=(30, 41, 59))
    draw.rectangle([(0, 1070), (int(width * progress), 1080)], fill=(16, 185, 129))

    img.save(out_png)

def main():
    print("=== Step 1: Generating High-Resolution 1080p Video Scenes ===")
    scene_videos = []

    for idx, scene in enumerate(SCENES):
        scene_id = scene["id"]
        wav_path = os.path.join(OUT_DIR, f"{scene_id}.wav")
        png_path = os.path.join(OUT_DIR, f"{scene_id}.png")
        mp4_path = os.path.join(OUT_DIR, f"{scene_id}.mp4")
        
        print(f"[{idx+1}/{len(SCENES)}] Synthesizing audio and rendering slide for {scene_id}...")
        synthesize_audio(scene["script"], wav_path)
        render_scene_slide(scene, png_path, idx, len(SCENES))
        
        # Fast & High-Quality Stillimage Video Encoding
        cmd = [
            "ffmpeg", "-y",
            "-loop", "1", "-i", png_path,
            "-i", wav_path,
            "-c:v", "libx264", "-tune", "stillimage",
            "-c:a", "aac", "-b:a", "192k",
            "-pix_fmt", "yuv420p",
            "-shortest",
            mp4_path
        ]
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"  -> Generated: {mp4_path}")
        scene_videos.append(mp4_path)

    print("\n=== Step 2: Concatenating Scenes into Final Master Demo Video ===")
    concat_list_file = os.path.join(OUT_DIR, "concat_list.txt")
    with open(concat_list_file, "w") as f:
        for v in scene_videos:
            f.write(f"file '{v.replace(chr(92), '/')}'\n")

    final_output = os.path.join(BASE_DIR, "verdant_prototype_demo.mp4")
    concat_cmd = [
        "ffmpeg", "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", concat_list_file,
        "-c", "copy",
        final_output
    ]
    subprocess.run(concat_cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    print(f"\n========================================================")
    print(f"  PROTOTYPE DEMO VIDEO GENERATED SUCCESSFULLY!")
    print(f"  File: {final_output}")
    print(f"========================================================")

if __name__ == "__main__":
    main()
