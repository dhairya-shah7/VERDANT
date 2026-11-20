"""
Google AI Tools Slide Generator for V.E.R.D.A.N.T.
Creates a high-resolution 1920x1080 presentation slide graphic for Slide 6 of the
Google DeepMind & Google Cloud Startup Buildathon India 2026 deck.
Covers: Google Antigravity, Google Agent Skills, Google AI Studio, and Google Cloud Run.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1920, 1080
img = Image.new("RGBA", (W, H), (248, 250, 252, 255))
draw = ImageDraw.Draw(img)

# Typography
font_title = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 36)
font_sub = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 15)
font_card_title = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 19)
font_card_badge = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 11)
font_section_h = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 12)
font_body = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 13)
font_body_b = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 13)
font_badge = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 12)
font_tag = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 10)
font_code = ImageFont.truetype("C:/Windows/Fonts/consola.ttf", 11)
font_code_b = ImageFont.truetype("C:/Windows/Fonts/consolab.ttf", 11)

# 1. Main Canvas Card Outline with Shadow
margin = 25
draw.rounded_rectangle([margin, margin, W - margin, H - margin], radius=20, fill=(255, 255, 255), outline=(226, 232, 240), width=2)

# 2. Header Section
head_x, head_y = 65, 50

# Google AI Quad-color accent bar
g_colors = [(66, 133, 244), (234, 67, 53), (251, 188, 5), (52, 168, 83)] # Google Blue, Red, Yellow, Green
for i, gc in enumerate(g_colors):
    draw.rounded_rectangle([head_x + i * 12, head_y, head_x + i * 12 + 8, head_y + 36], radius=4, fill=gc)

draw.text((head_x + 60, head_y - 6), "Google AI Tools Ecosystem", fill=(15, 23, 42), font=font_title)
draw.text((head_x + 62, head_y + 40), "Google AI Studio, Google Antigravity & Agent Skills Powering V.E.R.D.A.N.T. Pipeline", fill=(100, 116, 139), font=font_sub)

# Top Right Badges
rb_y = head_y + 2
b1_w = 265
b1_x = W - margin - b1_w - 50
draw.rounded_rectangle([b1_x, rb_y, b1_x + b1_w, rb_y + 36], radius=18, fill=(240, 253, 244), outline=(187, 247, 208), width=1)
draw.text((b1_x + 18, rb_y + 9), "Google Cloud & DeepMind 2026", fill=(21, 128, 61), font=font_badge)

b2_w = 205
b2_x = b1_x - b2_w - 14
draw.rounded_rectangle([b2_x, rb_y, b2_x + b2_w, rb_y + 36], radius=18, fill=(239, 246, 255), outline=(191, 219, 254), width=1)
draw.text((b2_x + 16, rb_y + 9), "● 100% Google AI Native", fill=(29, 78, 216), font=font_badge)

# Header divider
draw.line([(head_x, head_y + 78), (W - head_x, head_y + 78)], fill=(241, 245, 249), width=1)

# 3. 4-Column Core Grid Layout for the Tools
# Columns:
# Col 1: Google Antigravity (Orchestration & Agentic Lifecycle)
# Col 2: Google Agent Skills (Modular Capabilities & Distillation)
# Col 3: Google AI Studio (Prompt Design & Structured Outputs)
# Col 4: Google Cloud Run & Infra (Serverless Sandboxes & Telemetry)

cols = [
    {
        "id": "TOOL 01",
        "name": "Google Antigravity",
        "role": "Agentic Orchestration & Lifecycle",
        "tag": "CORE ORCHESTRATOR",
        "badge": "ACTIVE RUNTIME",
        "color": (66, 133, 244), # Google Blue
        "bg_pill": (239, 246, 255),
        "bullets": [
            ("Multi-Agent Handoffs: ", "Orchestrates seamless task transitions between ingestion, arbiter, and test synthesis agents."),
            ("Subagent Isolation: ", "Spawns ephemeral subagents for deep AST inspection and visual verification without polluting main context."),
            ("Reactive Event System: ", "Eliminates active polling loops with event-driven wakeups upon video frame and network log ingest."),
            ("Artifact Pipeline: ", "Persists verified PR payloads, test specs, and execution evidence in structured ledger directories.")
        ],
        "tech_chip": "google-antigravity-sdk · multi-agent-runtime"
    },
    {
        "id": "TOOL 02",
        "name": "Google Agent Skills",
        "role": "Modular Capability Contracts",
        "tag": "SKILL ECOSYSTEM",
        "badge": "EXTENSIBLE AGENT SKILLS",
        "color": (52, 168, 83), # Google Green
        "bg_pill": (240, 253, 244),
        "bullets": [
            ("AST Distillation Skill: ", "Automates AST interface skeletonization to slash prompt payload sizes by -84.9%."),
            ("Playwright Replay Skill: ", "Generates self-contained, accessible test specs from correlated DOM action anchors."),
            ("VERDE ESG Carbon Skill: ", "Calculates hardware-level Joules, PUE 1.10 efficiency, and water consumption metrics."),
            ("Verification-First Loop: ", "Enforces strict RED-then-GREEN automated testing gates prior to PR generation.")
        ],
        "tech_chip": "custom-agent-skills · SKILL.md specification"
    },
    {
        "id": "TOOL 03",
        "name": "Google AI Studio",
        "role": "Prompt Prototyping & Schema Tuning",
        "tag": "MODEL DESIGN PLATFORM",
        "badge": "STRUCTURED JSON",
        "color": (234, 67, 53), # Google Red
        "bg_pill": (254, 242, 242),
        "bullets": [
            ("Strict Schema Design: ", "Engineered typed Pydantic JSON contracts (`application/json`) preventing free-form model hallucinations."),
            ("System Prompt Tuning: ", "Iteratively benchmarked failure anchor prompts to maximize zero-shot root-cause accuracy."),
            ("Few-Shot Exemplars: ", "Calibrated model responses against verified real-world silent UI freezes and auth drops."),
            ("Latency Benchmarking: ", "Tuned system prompts to achieve sub-2.4s TTFT on Gemini 3.1 Flash-Lite.")
        ],
        "tech_chip": "Google AI Studio API · JSON Schema Enforcement"
    },
    {
        "id": "TOOL 04",
        "name": "Google Cloud Run",
        "role": "Serverless Infrastructure & Sandbox",
        "tag": "ZERO-COST SCALING",
        "badge": "CLOUD RUN & GCS",
        "color": (251, 188, 5), # Google Yellow / Amber
        "bg_pill": (254, 252, 232),
        "bullets": [
            ("Zero-Scale Architecture: ", "Runs FastAPI backend serverlessly on Cloud Run with automatic scale-to-zero when idle ($0 cost)."),
            ("Containerized Playwright: ", "Hosts isolated non-root Docker sandboxes (`node:20-bookworm-slim`) for hermetic test execution."),
            ("GCS Artifact Bucket: ", "Securely archives scrubbed HAR traces and encrypted MP4 screen recordings with automatic TTL expiry."),
            ("Google ESG Telemetry: ", "Integrates directly with Google Cloud's 1.10 PUE and 1.80 L/kWh carbon & cooling metrics.")
        ],
        "tech_chip": "Cloud Run Serverless · GCS Storage · Docker Sandbox"
    }
]

# Layout dimensions
card_w = 422
card_h = 580
card_y = 155
spacing = 18

for idx, col in enumerate(cols):
    cx = head_x + idx * (card_w + spacing)
    color = col["color"]
    
    # Shadow
    draw.rounded_rectangle([cx + 3, card_y + 4, cx + card_w + 3, card_y + card_h + 4], radius=16, fill=(235, 240, 246))
    # Card surface
    draw.rounded_rectangle([cx, card_y, cx + card_w, card_y + card_h], radius=16, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    
    # Top Accent Strip (Google Brand color for this card)
    draw.rounded_rectangle([cx, card_y, cx + card_w, card_y + 10], radius=5, fill=color)
    draw.rectangle([cx, card_y + 5, cx + card_w, card_y + 10], fill=color)
    
    # Card Header
    # Tool ID pill
    draw.rounded_rectangle([cx + 18, card_y + 22, cx + 18 + 72, card_y + 44], radius=6, fill=col["bg_pill"], outline=color, width=1)
    draw.text((cx + 26, card_y + 26), col["id"], fill=color, font=font_tag)
    
    # Badge (Status)
    draw.text((cx + card_w - 18 - draw.textbbox((0, 0), col["badge"], font=font_tag)[2], card_y + 27), col["badge"], fill=(100, 116, 139), font=font_tag)
    
    # Tool Title
    draw.text((cx + 18, card_y + 54), col["name"], fill=(15, 23, 42), font=font_card_title)
    # Role Subtitle
    draw.text((cx + 18, card_y + 82), col["role"].upper(), fill=color, font=font_section_h)
    
    # Divider
    draw.line([(cx + 18, card_y + 106), (cx + card_w - 18, card_y + 106)], fill=(241, 245, 249), width=1)
    
    # Bullets section
    by = card_y + 120
    draw.text((cx + 18, by), "INTEGRATION & IMPACT:", fill=(15, 23, 42), font=font_section_h)
    by += 24
    
    for lead, rest in col["bullets"]:
        # Bullet marker
        draw.ellipse([cx + 18, by + 4, cx + 24, by + 10], fill=color)
        draw.text((cx + 30, by), lead, fill=(15, 23, 42), font=font_body_b)
        lead_w = draw.textbbox((0, 0), lead, font=font_body_b)[2] - draw.textbbox((0, 0), lead, font=font_body_b)[0]
        
        # Word wrap remaining text
        words = rest.split()
        line1, line2 = "", ""
        for w in words:
            if len(lead + line1) + len(w) < 46:
                line1 += w + " "
            else:
                line2 += w + " "
                
        draw.text((cx + 30 + lead_w, by), line1.strip(), fill=(71, 85, 105), font=font_body)
        by += 20
        if line2:
            draw.text((cx + 30, by), line2.strip(), fill=(71, 85, 105), font=font_body)
            by += 20
        by += 8
        
    # Technical Stack Chip at bottom
    chip_y = card_y + card_h - 48
    draw.rounded_rectangle([cx + 16, chip_y, cx + card_w - 16, chip_y + 32], radius=8, fill=(248, 250, 252), outline=(226, 232, 240), width=1)
    draw.text((cx + 24, chip_y + 8), "SPEC: " + col["tech_chip"], fill=(71, 85, 105), font=font_code)

# 4. Horizontal Integration Pipeline Strip (Below Cards)
pipe_y = 755
pipe_w = W - 2 * head_x
draw.rounded_rectangle([head_x + 3, pipe_y + 4, head_x + pipe_w + 3, pipe_y + 230 + 4], radius=16, fill=(235, 240, 246))
draw.rounded_rectangle([head_x, pipe_y, head_x + pipe_w, pipe_y + 230], radius=16, fill=(255, 255, 255), outline=(226, 232, 240), width=1)

# Header strip of Integration Box
draw.rounded_rectangle([head_x, pipe_y, head_x + pipe_w, pipe_y + 36], radius=16, fill=(248, 250, 252))
draw.rectangle([head_x, pipe_y + 20, head_x + pipe_w, pipe_y + 36], fill=(248, 250, 252))
draw.line([(head_x, pipe_y + 36), (head_x + pipe_w, pipe_y + 36)], fill=(235, 240, 246), width=1)
draw.text((head_x + 20, pipe_y + 9), "Unified Google AI Architecture & Data Pipeline Flow", fill=(15, 23, 42), font=font_card_title)

# Flow steps across the bottom
flow_steps = [
    ("1. AI Studio", "Schema & Prompt Design", "Pydantic JSON contracts tune Gemini 3.1 for zero-hallucination failure mode detection."),
    ("2. Antigravity", "Multi-Agent Coordination", "Manages agent handoffs, subagent execution contexts, and persistent artifact ledgers."),
    ("3. Agent Skills", "Modular Tool Execution", "Executes OpenCV distillation (-84.9% tokens), AST pruning, and Playwright test writing."),
    ("4. Cloud Run", "Serverless Verification", "Runs hermetic Docker sandboxes for RED-to-GREEN replay testing at $0 idle cost.")
]

step_w = 410
for i, (stitle, srole, sdesc) in enumerate(flow_steps):
    sx = head_x + 20 + i * (step_w + 22)
    sy = pipe_y + 52
    
    # Step box
    draw.rounded_rectangle([sx, sy, sx + step_w, sy + 155], radius=10, fill=(248, 250, 252), outline=(226, 232, 240), width=1)
    
    # Step header
    bar_color = g_colors[i % len(g_colors)]
    draw.rounded_rectangle([sx + 14, sy + 14, sx + 22, sy + 36], radius=3, fill=bar_color)
    draw.text((sx + 30, sy + 14), stitle, fill=(15, 23, 42), font=font_body_b)
    draw.text((sx + 30, sy + 34), srole.upper(), fill=bar_color, font=font_tag)
    
    draw.line([(sx + 14, sy + 54), (sx + step_w - 14, sy + 54)], fill=(226, 232, 240), width=1)
    
    # Description
    words = sdesc.split()
    l1, l2, l3 = "", "", ""
    for w in words:
        if len(l1) + len(w) < 42:
            l1 += w + " "
        elif len(l2) + len(w) < 42:
            l2 += w + " "
        else:
            l3 += w + " "
    draw.text((sx + 14, sy + 64), l1.strip(), fill=(71, 85, 105), font=font_body)
    draw.text((sx + 14, sy + 84), l2.strip(), fill=(71, 85, 105), font=font_body)
    if l3:
        draw.text((sx + 14, sy + 104), l3.strip(), fill=(71, 85, 105), font=font_body)
        
    # Flow arrow between steps
    if i < len(flow_steps) - 1:
        ax = sx + step_w + 5
        ay = sy + 75
        draw.polygon([(ax + 12, ay), (ax, ay - 6), (ax, ay + 6)], fill=(148, 163, 184))

# 5. Footer Bar
foot_y = H - margin - 35
draw.line([(head_x, foot_y - 10), (W - head_x, foot_y - 10)], fill=(241, 245, 249), width=1)
draw.text((head_x, foot_y), "V.E.R.D.A.N.T. Google AI Tools Architecture · Startup Buildathon India 2026", fill=(100, 116, 139), font=font_sub)

status_txt = "Google Tech Stack: 100% Operational & Verified"
bbox = draw.textbbox((0, 0), status_txt, font=font_code_b)
tw = bbox[2] - bbox[0]
draw.text((W - head_x - tw, foot_y), status_txt, fill=(16, 185, 129), font=font_code_b)

# Save Outputs
out_buildathon = "C:/Users/Dhairya/Desktop/Active/Buildathon/google_ai_tools_verdant.png"
out_desktop = "C:/Users/Dhairya/Desktop/google_ai_tools_verdant.png"
img.save(out_buildathon, "PNG")
img.save(out_desktop, "PNG")

print(f"Successfully generated Google AI Tools slide at:\n  - {out_buildathon}\n  - {out_desktop}")
