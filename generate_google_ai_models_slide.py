"""
Google AI Models Slide Generator for V.E.R.D.A.N.T. (Matching Slide Theme)
Produces a clean, high-resolution 1920x1080 presentation slide graphic for Slide 7.
Matches the exact enterprise aesthetic of the other slides:
- Soft white canvas with rounded corners and subtle drop shadows
- Clean modern cards with subtle depth
- Explicit mapping of WHERE EACH MODEL IS USED across V.E.R.D.A.N.T. stages
- Structured technical specs, latency benchmarks, and data flow
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1920, 1080
img = Image.new("RGBA", (W, H), (248, 250, 252, 255))
draw = ImageDraw.Draw(img)

# Typography
font_title = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 36)
font_sub = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 15)
font_card_title = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 18)
font_card_badge = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 11)
font_section_h = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 11)
font_body = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 12)
font_body_b = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 12)
font_badge = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 12)
font_tag = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 10)
font_code = ImageFont.truetype("C:/Windows/Fonts/consola.ttf", 11)
font_code_b = ImageFont.truetype("C:/Windows/Fonts/consolab.ttf", 11)

# 1. Main Canvas Card Outline with Shadow
margin = 25
draw.rounded_rectangle([margin, margin, W - margin, H - margin], radius=20, fill=(255, 255, 255), outline=(226, 232, 240), width=2)

# 2. Header Section
head_x, head_y = 65, 50

# Google Quad-color accent bar
g_colors = [(66, 133, 244), (234, 67, 53), (251, 188, 5), (52, 168, 83)]
for i, gc in enumerate(g_colors):
    draw.rounded_rectangle([head_x + i * 12, head_y, head_x + i * 12 + 8, head_y + 36], radius=4, fill=gc)

draw.text((head_x + 60, head_y - 6), "Google AI Models Architecture", fill=(15, 23, 42), font=font_title)
draw.text((head_x + 62, head_y + 40), "Google AI Model Selection & Concrete Stage-by-Stage Usage Across V.E.R.D.A.N.T.", fill=(100, 116, 139), font=font_sub)

# Top Right Badges
rb_y = head_y + 2
b1_w = 265
b1_x = W - margin - b1_w - 50
draw.rounded_rectangle([b1_x, rb_y, b1_x + b1_w, rb_y + 36], radius=18, fill=(240, 253, 244), outline=(187, 247, 208), width=1)
draw.text((b1_x + 18, rb_y + 9), "Google Cloud & DeepMind 2026", fill=(21, 128, 61), font=font_badge)

b2_w = 205
b2_x = b1_x - b2_w - 14
draw.rounded_rectangle([b2_x, rb_y, b2_x + b2_w, rb_y + 36], radius=18, fill=(239, 246, 255), outline=(191, 219, 254), width=1)
draw.text((b2_x + 16, rb_y + 9), "● Verified Live Model Calls", fill=(29, 78, 216), font=font_badge)

# Header divider
draw.line([(head_x, head_y + 78), (W - head_x, head_y + 78)], fill=(241, 245, 249), width=1)

# 3. 3-Card Core Grid (The Models & Where They Are Used)
# Model 1: Gemini 3.1 Flash-Lite (Core Production Engine)
# Model 2: Gemini 3.1 Multimodal Vision (Visual Grounding Engine)
# Model 3: Gemini Structured JSON Schema Engine (Deterministic Arbiter & Code Synthesizer)

models = [
    {
        "id": "MODEL 01 · ACTIVE",
        "name": "Gemini 3.1 Flash-Lite",
        "role": "High-Throughput Semantic Reasoner",
        "where_stage": "STAGE 02: APEXTRACE (ENGINE A)",
        "where_desc": "Used as the primary analytical engine in ApexTrace. Takes sanitized AST skeletons, HTTP HAR logs, and console stack traces to diagnose failure anchors and hypothesize root cause within 2.4 seconds.",
        "badge": "PRODUCTION CORE",
        "color": (66, 133, 244), # Google Blue
        "bg_pill": (239, 246, 255),
        "bullets": [
            ("Sub-2.4s TTFT Latency: ", "Ultra-fast response time prevents pipeline lag during autonomous triage."),
            ("AST Interface Reasoning: ", "Operates on skeletonized code interfaces, maximizing reasoning efficiency."),
            ("Low Energy Profile: ", "Consumes only 0.28 Wh per execution, enabling 99.7% energy reduction."),
            ("Zero Model Drift: ", "Consistent failure classification across multiple test runs.")
        ],
        "spec": "gemini-3.1-flash-lite · Low-temperature (0.2) · JSON mode"
    },
    {
        "id": "MODEL 02 · HYBRID",
        "name": "Gemini Multimodal Vision",
        "role": "Temporal Video & Visual Grounding",
        "where_stage": "STAGE 01 & 02: CONTEXTPRISM & APEXTRACE",
        "where_desc": "Used during video ingestion and visual cross-validation. Analyzes user screen recording keyframes to correlate mouse clicks and UI freezes directly with network request drops and DOM elements.",
        "badge": "VISUAL ALIGNMENT",
        "color": (147, 51, 234), # Purple / Violet
        "bg_pill": (250, 245, 255),
        "bullets": [
            ("Temporal Frame Understanding: ", "Interprets sequential UI states before and after failure timestamps."),
            ("DOM-to-Pixel Grounding: ", "Translates visual click locations into semantic button and input targets."),
            ("Silent Freeze Detection: ", "Cross-validates visual state changes against expected network responses."),
            ("Token-Pruned Input: ", "Receives only OpenCV delta keyframes to avoid video context bloat.")
        ],
        "spec": "gemini-3.1-pro-vision / multimodal · Keyframe sequences"
    },
    {
        "id": "MODEL 03 · DETERMINISTIC",
        "name": "Gemini Structured Decoders",
        "role": "Typed Schema & Patch Synthesizer",
        "where_stage": "STAGE 03 & 04: ARBITER & REPLAY SHIELD",
        "where_desc": "Used in the Consensus Arbiter and Replay Shield. Enforces strict Pydantic JSON contracts to emit deterministic defect verdicts, Playwright test scripts (.spec.ts), and AST patch diffs (.patch).",
        "badge": "ZERO-HALLUCINATION",
        "color": (13, 148, 136), # Emerald / Teal
        "bg_pill": (240, 253, 250),
        "bullets": [
            ("Strict Schema Enforcement: ", "Locks output to typed JSON schemas, eliminating conversational filler."),
            ("Playwright Test Synthesis: ", "Generates executable accessibility locators (getByRole, getByTestId)."),
            ("Unified Diff Generation: ", "Outputs surgical, single-line code patches ready for sandbox testing."),
            ("Bayesian Confidence: ", "Calculates numeric confidence score (e.g., 94.8%) for PR evidence.")
        ],
        "spec": "Pydantic Schema Decoders · Strict response_mime_type"
    }
]

card_w = 566
card_h = 575
card_y = 155
spacing = 26

for idx, m in enumerate(models):
    cx = head_x + idx * (card_w + spacing)
    color = m["color"]
    
    # Soft drop shadow
    draw.rounded_rectangle([cx + 3, card_y + 4, cx + card_w + 3, card_y + card_h + 4], radius=16, fill=(235, 240, 246))
    # Card surface
    draw.rounded_rectangle([cx, card_y, cx + card_w, card_y + card_h], radius=16, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    
    # Top Accent Strip
    draw.rounded_rectangle([cx, card_y, cx + card_w, card_y + 10], radius=5, fill=color)
    draw.rectangle([cx, card_y + 5, cx + card_w, card_y + 10], fill=color)
    
    # Card Header
    # ID pill
    draw.rounded_rectangle([cx + 18, card_y + 22, cx + 18 + 125, card_y + 44], radius=6, fill=m["bg_pill"], outline=color, width=1)
    draw.text((cx + 26, card_y + 26), m["id"], fill=color, font=font_tag)
    
    # Badge (Status)
    draw.text((cx + card_w - 18 - draw.textbbox((0, 0), m["badge"], font=font_tag)[2], card_y + 27), m["badge"], fill=(100, 116, 139), font=font_tag)
    
    # Model Title
    draw.text((cx + 18, card_y + 54), m["name"], fill=(15, 23, 42), font=font_card_title)
    # Role Subtitle
    draw.text((cx + 18, card_y + 82), m["role"].upper(), fill=color, font=font_section_h)
    
    # Divider
    draw.line([(cx + 18, card_y + 104), (cx + card_w - 18, card_y + 104)], fill=(241, 245, 249), width=1)
    
    # WHERE IT IS USED SECTION (Prominent Highlight Box)
    wy = card_y + 116
    draw.rounded_rectangle([cx + 18, wy, cx + card_w - 18, wy + 90], radius=8, fill=(248, 250, 252), outline=(226, 232, 240), width=1)
    # Left colored accent line inside box
    draw.rounded_rectangle([cx + 18, wy, cx + 22, wy + 90], radius=2, fill=color)
    
    draw.text((cx + 32, wy + 8), "WHERE IT IS USED IN V.E.R.D.A.N.T.:", fill=(15, 23, 42), font=font_section_h)
    draw.text((cx + 32, wy + 26), m["where_stage"], fill=color, font=font_code_b)
    
    # Word wrap description
    words = m["where_desc"].split()
    l1, l2, l3 = "", "", ""
    for w in words:
        if len(l1) + len(w) < 56:
            l1 += w + " "
        elif len(l2) + len(w) < 56:
            l2 += w + " "
        else:
            l3 += w + " "
    draw.text((cx + 32, wy + 44), l1.strip(), fill=(71, 85, 105), font=font_body)
    draw.text((cx + 32, wy + 59), l2.strip(), fill=(71, 85, 105), font=font_body)
    if l3:
        draw.text((cx + 32, wy + 74), l3.strip(), fill=(71, 85, 105), font=font_body)
        
    # BULLETS SECTION
    by = wy + 104
    draw.text((cx + 18, by), "CAPABILITIES & BENCHMARKS:", fill=(15, 23, 42), font=font_section_h)
    by += 22
    
    for lead, rest in m["bullets"]:
        draw.ellipse([cx + 18, by + 4, cx + 24, by + 10], fill=color)
        draw.text((cx + 30, by), lead, fill=(15, 23, 42), font=font_body_b)
        lead_w = draw.textbbox((0, 0), lead, font=font_body_b)[2] - draw.textbbox((0, 0), lead, font=font_body_b)[0]
        
        words = rest.split()
        bline1, bline2 = "", ""
        for w in words:
            if len(lead + bline1) + len(w) < 54:
                bline1 += w + " "
            else:
                bline2 += w + " "
        draw.text((cx + 30 + lead_w, by), bline1.strip(), fill=(71, 85, 105), font=font_body)
        by += 18
        if bline2:
            draw.text((cx + 30, by), bline2.strip(), fill=(71, 85, 105), font=font_body)
            by += 18
        by += 6
        
    # Technical Spec Chip at bottom
    chip_y = card_y + card_h - 46
    draw.rounded_rectangle([cx + 16, chip_y, cx + card_w - 16, chip_y + 30], radius=6, fill=(248, 250, 252), outline=(226, 232, 240), width=1)
    draw.text((cx + 24, chip_y + 7), "CONFIG: " + m["spec"], fill=(71, 85, 105), font=font_code)

# 4. Horizontal Model Orchestration Flow (Bottom Section)
flow_y = 755
flow_w = W - 2 * head_x
draw.rounded_rectangle([head_x + 3, flow_y + 4, head_x + flow_w + 3, flow_y + 230 + 4], radius=16, fill=(235, 240, 246))
draw.rounded_rectangle([head_x, flow_y, head_x + flow_w, flow_y + 230], radius=16, fill=(255, 255, 255), outline=(226, 232, 240), width=1)

# Header
draw.rounded_rectangle([head_x, flow_y, head_x + flow_w, flow_y + 36], radius=16, fill=(248, 250, 252))
draw.rectangle([head_x, flow_y + 20, head_x + flow_w, flow_y + 36], fill=(248, 250, 252))
draw.line([(head_x, flow_y + 36), (head_x + flow_w, flow_y + 36)], fill=(235, 240, 246), width=1)
draw.text((head_x + 20, flow_y + 9), "End-to-End Google AI Model Execution & Fallback Pipeline", fill=(15, 23, 42), font=font_card_title)

flow_boxes = [
    ("Stage 01: Ingestion", "Gemini Multimodal", "Samples keyframes, maps temporal clicks, and correlates video timeline to HAR network timestamps.", (147, 51, 234)),
    ("Stage 02: Analysis", "Gemini 3.1 Flash-Lite", "Ingests AST skeletons & HAR logs; hypothesizes failure root-cause in 2.4s without context bloat.", (66, 133, 244)),
    ("Stage 03: Consensus", "Structured Decoders", "Applies 3-tier deterministic precedence to cross-validate AI hypothesis against SSIM pixel sentinel.", (13, 148, 136)),
    ("Stage 04: Sandbox Replay", "Gemini Code Engine", "Synthesizes executable Playwright test specs (.spec.ts) and verifies RED-to-GREEN patch diff.", (217, 119, 6))
]

s_w = 410
for i, (stage_name, model_used, desc, bar_col) in enumerate(flow_boxes):
    bx = head_x + 20 + i * (s_w + 22)
    by = flow_y + 52
    
    draw.rounded_rectangle([bx, by, bx + s_w, by + 155], radius=10, fill=(248, 250, 252), outline=(226, 232, 240), width=1)
    
    # Left colored accent bar
    draw.rounded_rectangle([bx + 14, by + 14, bx + 22, by + 36], radius=3, fill=bar_col)
    draw.text((bx + 30, by + 14), stage_name, fill=(15, 23, 42), font=font_body_b)
    draw.text((bx + 30, by + 34), model_used.upper(), fill=bar_col, font=font_tag)
    
    draw.line([(bx + 14, by + 54), (bx + s_w - 14, by + 54)], fill=(226, 232, 240), width=1)
    
    # Description wrap
    words = desc.split()
    w1, w2, w3 = "", "", ""
    for w in words:
        if len(w1) + len(w) < 42:
            w1 += w + " "
        elif len(w2) + len(w) < 42:
            w2 += w + " "
        else:
            w3 += w + " "
    draw.text((bx + 14, by + 64), w1.strip(), fill=(71, 85, 105), font=font_body)
    draw.text((bx + 14, by + 84), w2.strip(), fill=(71, 85, 105), font=font_body)
    if w3:
        draw.text((bx + 14, by + 104), w3.strip(), fill=(71, 85, 105), font=font_body)
        
    # Connector arrow
    if i < len(flow_boxes) - 1:
        arr_x = bx + s_w + 5
        arr_y = by + 75
        draw.polygon([(arr_x + 12, arr_y), (arr_x, arr_y - 6), (arr_x, arr_y + 6)], fill=(148, 163, 184))

# 5. Footer Bar
foot_y = H - margin - 35
draw.line([(head_x, foot_y - 10), (W - head_x, foot_y - 10)], fill=(241, 245, 249), width=1)
draw.text((head_x, foot_y), "V.E.R.D.A.N.T. Google AI Models Blueprint · Startup Buildathon India 2026", fill=(100, 116, 139), font=font_sub)

status_txt = "Gemini 3.1 Flash-Lite: Verified Live & Operational"
bbox = draw.textbbox((0, 0), status_txt, font=font_code_b)
tw = bbox[2] - bbox[0]
draw.text((W - head_x - tw, foot_y), status_txt, fill=(16, 185, 129), font=font_code_b)

# Save Outputs
out_buildathon = "C:/Users/Dhairya/Desktop/Active/Buildathon/google_ai_models_verdant.png"
out_desktop = "C:/Users/Dhairya/Desktop/google_ai_models_verdant.png"
img.save(out_buildathon, "PNG")
img.save(out_desktop, "PNG")

print(f"Successfully generated Google AI Models slide at:\n  - {out_buildathon}\n  - {out_desktop}")
