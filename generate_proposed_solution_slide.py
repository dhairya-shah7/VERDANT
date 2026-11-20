"""
Proposed Solution Slide Generator for V.E.R.D.A.N.T. (Slide 4)
Builds a high-impact presentation slide based on the 3-segment circular donut architecture:
- Left Half: Structured Problem-to-Solution Mapping & 3-Pillar Breakdown
- Right Half: High-Impact 3-Segment Donut Wheel with glowing icons, percentage badges, and central Gemini core
"""
import os
import math
from PIL import Image, ImageDraw, ImageFont

W, H = 1920, 1080
img = Image.new("RGBA", (W, H), (248, 250, 252, 255))
draw = ImageDraw.Draw(img)

# Typography
font_title = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 36)
font_sub = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 15)
font_pillar_title = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 18)
font_pillar_role = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 12)
font_body = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 13)
font_body_b = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 13)
font_tag = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 11)
font_badge = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 12)
font_donut_lbl = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 15)
font_donut_sub = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 12)
font_hub_title = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 20)
font_hub_sub = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 11)
font_code_b = ImageFont.truetype("C:/Windows/Fonts/consolab.ttf", 11)

# 1. Subtle Background Grid
grid_step = 40
for gx in range(0, W, grid_step):
    draw.line([(gx, 0), (gx, H)], fill=(241, 245, 249), width=1)
for gy in range(0, H, grid_step):
    draw.line([(0, gy), (W, gy)], fill=(241, 245, 249), width=1)

# 2. Main Outer Card
margin = 25
draw.rounded_rectangle([margin, margin, W - margin, H - margin], radius=22, fill=(255, 255, 255), outline=(226, 232, 240), width=2)

# 3. Header Section
head_x, head_y = 65, 48
g_colors = [(66, 133, 244), (234, 67, 53), (251, 188, 5), (52, 168, 83)]
for i, gc in enumerate(g_colors):
    draw.rounded_rectangle([head_x + i * 12, head_y, head_x + i * 12 + 8, head_y + 36], radius=4, fill=gc)

draw.text((head_x + 60, head_y - 6), "Proposed Solution: V.E.R.D.A.N.T.", fill=(15, 23, 42), font=font_title)
draw.text((head_x + 62, head_y + 40), "Autonomous Bug Reproduction, Dual-Engine Consensus & Green Closed-Loop TDD Pipeline", fill=(100, 116, 139), font=font_sub)

# Top Right Badges
rb_y = head_y + 2
b1_w = 265
b1_x = W - margin - b1_w - 50
draw.rounded_rectangle([b1_x, rb_y, b1_x + b1_w, rb_y + 36], radius=18, fill=(240, 253, 244), outline=(187, 247, 208), width=1)
draw.text((b1_x + 18, rb_y + 9), "Google Cloud & DeepMind 2026", fill=(21, 128, 61), font=font_badge)

b2_w = 195
b2_x = b1_x - b2_w - 14
draw.rounded_rectangle([b2_x, rb_y, b2_x + b2_w, rb_y + 36], radius=18, fill=(239, 246, 255), outline=(191, 219, 254), width=1)
draw.text((b2_x + 16, rb_y + 9), "● 3-Pillar Solution Triad", fill=(29, 78, 216), font=font_badge)

draw.line([(head_x, head_y + 78), (W - head_x, head_y + 78)], fill=(241, 245, 249), width=1)

# 4. Layout: Left Text & Pillar Cards (x: 65 to 980), Right Donut Triad Visual (x: 1020 to 1855)
left_w = 915
left_y = 150
left_h = 825

# Overview Banner on Left
draw.rounded_rectangle([head_x, left_y, head_x + left_w, left_y + 80], radius=12, fill=(248, 250, 252), outline=(226, 232, 240), width=1)
draw.text((head_x + 18, left_y + 14), "THE CLOSED-LOOP AUTONOMOUS QA PARADIGM", fill=(29, 78, 216), font=font_tag)
draw.text((head_x + 18, left_y + 32), "V.E.R.D.A.N.T. eliminates developer bug reproduction toil through a 3-pillar architecture:", fill=(15, 23, 42), font=font_body_b)
draw.text((head_x + 18, left_y + 52), "Zero-Trust Distillation ➔ Dual-Engine Consensus ➔ Hermetic Verification & Green GitOps.", fill=(71, 85, 105), font=font_body)

# 3 Solution Pillar Cards on Left
pillars = [
    {
        "id": "PILLAR 01",
        "title": "Zero-Trust Context Distillation (ContextPrism)",
        "role": "SOLVES: CONTEXT BLOAT & PII EXPOSURE",
        "tag": "-84.9% TOKEN REDUCTION · ZERO PII LEAKS",
        "color": (14, 116, 144), # Cyan / Blue
        "bullets": [
            ("OpenCV 4.10 Delta Sampling: ", "Discards idle 60fps frames; extracts only critical visual transition moments."),
            ("Regex Security Perimeter: ", "Sanitizes Bearer JWTs, auth cookies, and passwords before any LLM ingestion."),
            ("AST Interface Skeletonizer: ", "Prunes heavy code bodies to retain pure interface signatures, stopping model degradation.")
        ]
    },
    {
        "id": "PILLAR 02",
        "title": "Dual-Engine Consensus Arbiter (ApexTrace)",
        "role": "SOLVES: AI HALLUCINATIONS & SILENT FREEZES",
        "tag": "100% FALSE-POSITIVE REJECTION · 94.8% CONF",
        "color": (217, 119, 6), # Amber / Orange
        "bullets": [
            ("Bimodal AI Reasoning: ", "Gemini 3.1 Flash-Lite analyzes AST code & network timelines in sub-2.4s TTFT."),
            ("Mathematical Sentinel: ", "Pillow SSIM covariance (<0.92) and pixel-delta (<0.02%) probe for silent UI freezes."),
            ("3-Tier Precedence Arbiter: ", "System HTTP 4xx/5xx errors rule with absolute priority over transient visual noise.")
        ]
    },
    {
        "id": "PILLAR 03",
        "title": "Hermetic TDD Replay & Green GitOps (Shield + Hydra)",
        "role": "SOLVES: UNTESTED CODE & HUGE GPU CARBON",
        "tag": "CLOSED-LOOP RED➔GREEN · 99.7% ENERGY SAVED",
        "color": (15, 118, 110), # Deep Teal / Green
        "bullets": [
            ("Docker Sandbox Replay: ", "Synthesizes executable Playwright tests; verifies RED (bug fails) then GREEN (patch passes)."),
            ("Google Cloud ESG Audit: ", "Tracks PUE 1.10 and WUE 1.80 L/kWh standards (0.28 Wh vs 90 Wh manual triage)."),
            ("Automated Pull Request: ", "Dispatches reviewer-ready GitHub Draft PRs with cryptographic reproduction evidence.")
        ]
    }
]

card_y = left_y + 98
card_h = 220
card_gap = 20

for idx, p in enumerate(pillars):
    py = card_y + idx * (card_h + card_gap)
    draw.rounded_rectangle([head_x + 2, py + 3, head_x + left_w + 2, py + card_h + 3], radius=14, fill=(235, 240, 246))
    draw.rounded_rectangle([head_x, py, head_x + left_w, py + card_h], radius=14, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    
    # Left colored vertical accent strip
    draw.rounded_rectangle([head_x, py, head_x + 6, py + card_h], radius=3, fill=p["color"])
    
    # Header strip inside card
    draw.rounded_rectangle([head_x + 6, py, head_x + left_w, py + 40], radius=14, fill=(248, 250, 252))
    draw.rectangle([head_x + 6, py + 22, head_x + left_w, py + 40], fill=(248, 250, 252))
    draw.line([(head_x + 6, py + 40), (head_x + left_w, py + 40)], fill=(235, 240, 246), width=1)
    
    # Pillar ID Pill
    draw.rounded_rectangle([head_x + 18, py + 8, head_x + 18 + 75, py + 30], radius=5, fill=(255, 255, 255), outline=p["color"], width=1)
    draw.text((head_x + 24, py + 12), p["id"], fill=p["color"], font=font_tag)
    
    draw.text((head_x + 105, py + 9), p["title"], fill=(15, 23, 42), font=font_pillar_title)
    
    # Role / Solves Subtitle
    draw.text((head_x + 18, py + 48), p["role"], fill=p["color"], font=font_pillar_role)
    
    # Badge
    bbox = draw.textbbox((0, 0), p["tag"], font=font_tag)
    tag_w = bbox[2] - bbox[0] + 16
    draw.rounded_rectangle([head_x + left_w - tag_w - 18, py + 46, head_x + left_w - 18, py + 68], radius=6, fill=(241, 245, 249))
    draw.text((head_x + left_w - tag_w - 10, py + 50), p["tag"], fill=(51, 65, 85), font=font_tag)
    
    # Bullets
    by = py + 78
    for lead, rest in p["bullets"]:
        draw.ellipse([head_x + 18, by + 4, head_x + 24, by + 10], fill=p["color"])
        draw.text((head_x + 30, by), lead, fill=(15, 23, 42), font=font_body_b)
        lead_w = draw.textbbox((0, 0), lead, font=font_body_b)[2] - draw.textbbox((0, 0), lead, font=font_body_b)[0]
        draw.text((head_x + 30 + lead_w, by), rest, fill=(71, 85, 105), font=font_body)
        by += 28

# -------------------------------------------------------------
# RIGHT HALF: THE 3-SEGMENT DONUT TRIAD (x: 1020 to 1855)
# -------------------------------------------------------------
right_w = W - margin - (head_x + left_w + 40) - 20
right_x = head_x + left_w + 40
donut_cx = right_x + right_w // 2
donut_cy = left_y + left_h // 2 + 10

# Outer & Inner Donut Radii
R_OUT = 250
R_IN = 135

# Segment Angles (3 equal 120-degree segments with a small gap)
# Segment 1 (Top-Right): -30 deg to 90 deg (or 0 to 120)
# Segment 2 (Bottom): 90 deg to 210 deg (120 to 240)
# Segment 3 (Top-Left): 210 deg to 330 deg (240 to 360)
gap_deg = 3.5

segments = [
    {
        "name": "PILLAR 01: DISTILL",
        "sub": "ContextPrism · Ingestion",
        "metric": "84.9% PRUNED",
        "start": -30 + gap_deg,
        "end": 90 - gap_deg,
        "color_outer": (14, 116, 144),  # Cyan
        "color_inner": (8, 145, 178),
        "label_pos": (donut_cx + 140, donut_cy - 70)
    },
    {
        "name": "PILLAR 02: CONSENSUS",
        "sub": "ApexTrace · Arbiter",
        "metric": "100% GATED",
        "start": 90 + gap_deg,
        "end": 210 - gap_deg,
        "color_outer": (217, 119, 6),   # Amber
        "color_inner": (245, 158, 11),
        "label_pos": (donut_cx - 10, donut_cy + 200)
    },
    {
        "name": "PILLAR 03: VERIFY",
        "sub": "Shield · Green GitOps",
        "metric": "99.7% SAVINGS",
        "start": 210 + gap_deg,
        "end": 330 - gap_deg,
        "color_outer": (15, 118, 110),  # Teal / Emerald
        "color_inner": (20, 184, 166),
        "label_pos": (donut_cx - 175, donut_cy - 70)
    }
]

# Draw Donut Segments with fine angular resolution
def draw_donut_slice(cx, cy, r_in, r_out, a_start, a_end, color, outline_col=(255, 255, 255)):
    points = []
    # Outer arc
    steps = 60
    for i in range(steps + 1):
        ang = math.radians(a_start + (a_end - a_start) * (i / steps))
        points.append((cx + r_out * math.cos(ang), cy + r_out * math.sin(ang)))
    # Inner arc (reverse)
    for i in range(steps + 1):
        ang = math.radians(a_end - (a_end - a_start) * (i / steps))
        points.append((cx + r_in * math.cos(ang), cy + r_in * math.sin(ang)))
    draw.polygon(points, fill=color, outline=outline_col)

# Drop shadow behind donut
for seg in segments:
    draw_donut_slice(donut_cx + 3, donut_cy + 5, R_IN, R_OUT, seg["start"], seg["end"], (226, 232, 240), outline_col=(226, 232, 240))

# Main Donut Slices
for seg in segments:
    draw_donut_slice(donut_cx, donut_cy, R_IN, R_OUT, seg["start"], seg["end"], seg["color_outer"], outline_col=(255, 255, 255))
    
    # Cross-hatching pattern / internal texture simulation (like template)
    mid_ang = math.radians((seg["start"] + seg["end"]) / 2)
    # Mid-radius marker
    mr = (R_IN + R_OUT) / 2
    px, py = donut_cx + mr * math.cos(mid_ang), donut_cy + mr * math.sin(mid_ang)
    
    # White metric badge on slice
    bbox = draw.textbbox((0, 0), seg["metric"], font=font_tag)
    bw = bbox[2] - bbox[0] + 16
    draw.rounded_rectangle([px - bw//2, py - 12, px + bw//2, py + 12], radius=6, fill=(255, 255, 255))
    draw.text((px - bw//2 + 8, py - 7), seg["metric"], fill=seg["color_outer"], font=font_tag)

# Central Hub (Hollow White Center with Google AI Core)
draw.ellipse([donut_cx - R_IN + 6, donut_cy - R_IN + 6, donut_cx + R_IN - 6, donut_cy + R_IN - 6], fill=(255, 255, 255), outline=(226, 232, 240), width=2)
draw.ellipse([donut_cx - R_IN + 16, donut_cy - R_IN + 16, donut_cx + R_IN - 16, donut_cy + R_IN - 16], fill=(248, 250, 252))

# Central Icon & Text
draw.polygon([
    (donut_cx, donut_cy - 48),
    (donut_cx + 12, donut_cy - 16),
    (donut_cx + 44, donut_cy - 4),
    (donut_cx + 12, donut_cy + 8),
    (donut_cx, donut_cy + 40),
    (donut_cx - 12, donut_cy + 8),
    (donut_cx - 44, donut_cy - 4),
    (donut_cx - 12, donut_cy - 16)
], fill=(66, 133, 244))

draw.text((donut_cx - 68, donut_cy - 10), "V.E.R.D.A.N.T.", fill=(15, 23, 42), font=font_hub_title)
draw.text((donut_cx - 78, donut_cy + 16), "Autonomous QA Core", fill=(100, 116, 139), font=font_hub_sub)
draw.text((donut_cx - 62, donut_cy + 34), "Google Cloud Native", fill=(21, 128, 61), font=font_tag)

# Callout labels around the donut
# Callout 1 (Top-Right: Pillar 1)
c1_x, c1_y = donut_cx + R_OUT + 15, donut_cy - 120
draw.line([(donut_cx + R_OUT * math.cos(math.radians(30)), donut_cy + R_OUT * math.sin(math.radians(30))), (c1_x, c1_y + 20)], fill=(14, 116, 144), width=2)
draw.text((c1_x + 8, c1_y), "01 · DISTILLATION", fill=(14, 116, 144), font=font_pillar_title)
draw.text((c1_x + 8, c1_y + 22), "OpenCV + AST Interface Skeletons", fill=(71, 85, 105), font=font_body)

# Callout 2 (Bottom: Pillar 2)
c2_x, c2_y = donut_cx - 120, donut_cy + R_OUT + 35
draw.line([(donut_cx, donut_cy + R_OUT), (donut_cx, c2_y)], fill=(217, 119, 6), width=2)
draw.text((c2_x - 10, c2_y + 8), "02 · CONSENSUS ARBITER", fill=(217, 119, 6), font=font_pillar_title)
draw.text((c2_x - 10, c2_y + 30), "Gemini 3.1 + SSIM Pixel Sentinel", fill=(71, 85, 105), font=font_body)

# Callout 3 (Top-Left: Pillar 3)
c3_x, c3_y = donut_cx - R_OUT - 180, donut_cy - 120
draw.line([(donut_cx + R_OUT * math.cos(math.radians(270)), donut_cy + R_OUT * math.sin(math.radians(270))), (c3_x + 160, c3_y + 20)], fill=(15, 118, 110), width=2)
draw.text((c3_x, c3_y), "03 · CLOSED-LOOP TDD", fill=(15, 118, 110), font=font_pillar_title)
draw.text((c3_x, c3_y + 22), "Playwright Replay & Green GitOps", fill=(71, 85, 105), font=font_body)

# 5. Footer
foot_y = H - margin - 35
draw.line([(head_x, foot_y - 10), (W - head_x, foot_y - 10)], fill=(241, 245, 249), width=1)
draw.text((head_x, foot_y), "V.E.R.D.A.N.T. 3-Pillar Solution Triad · Startup Buildathon India 2026", fill=(100, 116, 139), font=font_sub)

status_txt = "Closed-Loop TDD: Verified RED ➔ GREEN in Docker"
bbox = draw.textbbox((0, 0), status_txt, font=font_code_b)
tw = bbox[2] - bbox[0]
draw.text((W - head_x - tw, foot_y), status_txt, fill=(16, 185, 129), font=font_code_b)

# Save Outputs
out_buildathon = os.path.normpath(r"C:\Users\Dhairya\Desktop\Active\Buildathon\proposed_solution_verdant.png")
out_desktop = os.path.normpath(r"C:\Users\Dhairya\Desktop\proposed_solution_verdant.png")
img.save(out_buildathon, format="PNG")
img.save(out_desktop, format="PNG")

print(f"Successfully generated Proposed Solution slide at:\n  - {out_buildathon}\n  - {out_desktop}")
