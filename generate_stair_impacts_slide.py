"""
5-Step 3D Isometric Stair Slide Generator for V.E.R.D.A.N.T.
Slide 8: Impacts & Strategic Benefits
Creates a 1920x1080 high-resolution presentation slide matching the 5-Step Stair template.
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
font_step_num = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 13)
font_step_title = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 18)
font_metric = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 16)
font_body = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 13)
font_code = ImageFont.truetype("C:/Windows/Fonts/consolab.ttf", 11)
font_badge = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 12)
font_cube_num = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 18)

# 1. Subtle Background Grid & World Map Hint
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

draw.text((head_x + 60, head_y - 6), "Measurable Impacts & Strategic Benefits", fill=(15, 23, 42), font=font_title)
draw.text((head_x + 62, head_y + 40), "Quantifiable Engineering Velocity, Token Efficiency, and Net-Zero ESG Value · V.E.R.D.A.N.T.", fill=(100, 116, 139), font=font_sub)

# Badges
rb_y = head_y + 2
b1_w = 265
b1_x = W - margin - b1_w - 50
draw.rounded_rectangle([b1_x, rb_y, b1_x + b1_w, rb_y + 36], radius=18, fill=(240, 253, 244), outline=(187, 247, 208), width=1)
draw.text((b1_x + 18, rb_y + 9), "Google Cloud & DeepMind 2026", fill=(21, 128, 61), font=font_badge)

b2_w = 195
b2_x = b1_x - b2_w - 14
draw.rounded_rectangle([b2_x, rb_y, b2_x + b2_w, rb_y + 36], radius=18, fill=(239, 246, 255), outline=(191, 219, 254), width=1)
draw.text((b2_x + 16, rb_y + 9), "● 5-Step Value Escalation", fill=(29, 78, 216), font=font_badge)

draw.line([(head_x, head_y + 78), (W - head_x, head_y + 78)], fill=(241, 245, 249), width=1)

# 4. Content Definition (5 Steps)
steps = [
    {
        "id": "STEP 01",
        "title": "99.5% Faster Mean Time to Diagnose (MTTD)",
        "metric": "12.0s vs 45.0m Manual Triage",
        "desc": "Autonomous multimodal correlation cuts triage from ~45 minutes of manual video scrubbing to 12s.",
        "color": (234, 88, 12),  # Coral Orange
        "icon": "speed"
    },
    {
        "id": "STEP 02",
        "title": "84.9% Context Window & Token Reduction",
        "metric": "-84.9% Payload · Sub-2.4s TTFT",
        "desc": "AST interface skeletonizer strips implementation bloat, preventing hallucinations & slashing API costs.",
        "color": (217, 119, 6),  # Amber
        "icon": "chart"
    },
    {
        "id": "STEP 03",
        "title": "100% False-Positive Rejection via Arbiter",
        "metric": "Zero Hallucinations · 94.8% Conf",
        "desc": "3-tier consensus cross-checks visual glitches with hard network HTTP/DOM logs for zero false alerts.",
        "color": (66, 133, 244), # Google Blue
        "icon": "target"
    },
    {
        "id": "STEP 04",
        "title": "Hermetic Closed-Loop RED ➔ GREEN TDD Replay",
        "metric": "Automated Docker Playwright Proof",
        "desc": "Synthesizes executable Playwright tests, proving bug reproduction and patch correctness before review.",
        "color": (147, 51, 234), # Purple
        "icon": "brain"
    },
    {
        "id": "STEP 05",
        "title": "99.7% Energy, Carbon & Water Reduction (ESG)",
        "metric": "0.28 Wh vs 90 Wh · Verified Eco-Badge",
        "desc": "Cuts serverless compute cycles by 99.7% with certified Google Cloud PUE 1.10 and WUE audit badges on PRs.",
        "color": (16, 185, 129), # Emerald Green
        "icon": "leaf"
    }
]

# 5. Left Side: 5 Detailed Step Cards with Connectors
card_x = 75
card_w = 860
card_h = 138
gap = 26
start_card_y = 155

# Target anchor points for connecting lines to the stair on the right
stair_anchors = []

for i, s in enumerate(steps):
    cy = start_card_y + i * (card_h + gap)
    color = s["color"]
    
    # Outer Card with subtle shadow
    draw.rounded_rectangle([card_x + 3, cy + 3, card_x + card_w + 3, cy + card_h + 3], radius=14, fill=(235, 240, 246))
    draw.rounded_rectangle([card_x, cy, card_x + card_w, cy + card_h], radius=14, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    
    # Left colored vertical accent bar
    draw.rounded_rectangle([card_x, cy, card_x + 8, cy + card_h], radius=3, fill=color)
    
    # Step ID Pill
    pill_w = 80
    draw.rounded_rectangle([card_x + 22, cy + 14, card_x + 22 + pill_w, cy + 36], radius=6, fill=(color[0], color[1], color[2], 20), outline=color, width=1)
    draw.text((card_x + 32, cy + 17), s["id"], fill=color, font=font_step_num)
    
    # Title & Metric
    draw.text((card_x + 115, cy + 14), s["title"], fill=(15, 23, 42), font=font_step_title)
    
    # Metric badge on right side of card
    m_bbox = draw.textbbox((0, 0), s["metric"], font=font_code)
    mw = m_bbox[2] - m_bbox[0]
    draw.rounded_rectangle([card_x + card_w - mw - 30, cy + 13, card_x + card_w - 14, cy + 37], radius=6, fill=(248, 250, 252), outline=(203, 213, 225), width=1)
    draw.text((card_x + card_w - mw - 22, cy + 18), s["metric"], fill=color, font=font_code)
    
    # Description
    draw.text((card_x + 24, cy + 50), s["desc"], fill=(71, 85, 105), font=font_body)
    
    # Bottom key takeaway
    takeaways = [
        "Eliminates hours of manual debugging · Instant Root-Cause Identification",
        "Zero Lost-in-the-Middle context degradation · 85% lower LLM bill",
        "Strict 3-tier precedence hierarchy · 100% false-positive rejection",
        "Closed-loop RED ❌ to GREEN ✅ sandbox verification before PR creation",
        "Audited with Google Cloud PUE = 1.10 and cooling WUE = 1.80 L/kWh"
    ]
    draw.text((card_x + 24, cy + 85), f"✔ {takeaways[i]}", fill=(15, 23, 42), font=font_body)
    
    # Connector line right anchor
    conn_y = cy + card_h // 2
    draw.ellipse([card_x + card_w - 4, conn_y - 4, card_x + card_w + 4, conn_y + 4], fill=color)

# -------------------------------------------------------------------------
# 6. Right Side: 5-Step 3D Isometric Stair Graphic
# -------------------------------------------------------------------------
# Isometric projection parameters
# The stair ascends from Step 1 (bottom left of stair zone) to Step 5 (top right of stair zone)
stair_base_x = 1040
stair_base_y = 780
dx = 76   # step shift right-up in isometric plane
dy = -66  # step shift up
step_w = 175
step_d = 120
step_h = 75

for i in range(5):
    step_idx = i
    s = steps[step_idx]
    color = s["color"]
    
    # Step position
    sx = stair_base_x + i * dx
    sy = stair_base_y + i * dy
    
    # Draw step structure
    # Isometric vertices:
    # Front Face (Rectangle / Parallelogram)
    p_front_top_left = (sx, sy)
    p_front_top_right = (sx + step_w, sy)
    p_front_bot_right = (sx + step_w, sy + step_h)
    p_front_bot_left = (sx, sy + step_h)
    
    # Top Face (Isometric rhombus)
    # offset for depth: back goes up and slightly right
    dep_x = 90
    dep_y = -50
    p_top_back_left = (sx + dep_x, sy + dep_y)
    p_top_back_right = (sx + step_w + dep_x, sy + dep_y)
    
    # Side Face (Right side)
    p_side_bot_right = (sx + step_w + dep_x, sy + step_h + dep_y)
    
    # 1. Shadow under step
    draw.polygon([
        (sx - 10, sy + step_h + 10),
        (sx + step_w + dep_x + 10, sy + step_h + dep_y + 10),
        (sx + step_w + dep_x + 10, sy + step_h + dep_y + 25),
        (sx - 10, sy + step_h + 25)
    ], fill=(226, 232, 240, 180))
    
    # 2. Right Side Face (Darker Blue-Grey)
    draw.polygon([
        p_front_top_right,
        p_top_back_right,
        p_side_bot_right,
        p_front_bot_right
    ], fill=(148, 163, 184), outline=(100, 116, 139), width=1)
    
    # 3. Front Face (Slate Blue-Grey with Colored Front Accent Stripe)
    draw.polygon([
        p_front_top_left,
        p_front_top_right,
        p_front_bot_right,
        p_front_bot_left
    ], fill=(203, 213, 225), outline=(148, 163, 184), width=1)
    
    # Front Accent Inset Block (Matches template's orange block style)
    accent_w = 65
    accent_x1 = sx + (step_w - accent_w) // 2
    draw.polygon([
        (accent_x1, sy + 6),
        (accent_x1 + accent_w, sy + 6),
        (accent_x1 + accent_w, sy + step_h - 6),
        (accent_x1, sy + step_h - 6)
    ], fill=color)
    
    # 4. Top Face (Light Slate / Soft Tint)
    draw.polygon([
        p_front_top_left,
        p_top_back_left,
        p_top_back_right,
        p_front_top_right
    ], fill=(241, 245, 249), outline=(203, 213, 225), width=1)
    
    # 5. Floating 3D Cube / Metric Block on top of each step
    cube_cx = sx + step_w // 2 + dep_x // 2
    cube_cy = sy + dep_y // 2 - 20
    cw = 50
    ch = 44
    cdep_x = 22
    cdep_y = -14
    
    # Cube right face
    draw.polygon([
        (cube_cx + cw//2, cube_cy - ch//2),
        (cube_cx + cw//2 + cdep_x, cube_cy - ch//2 + cdep_y),
        (cube_cx + cw//2 + cdep_x, cube_cy + ch//2 + cdep_y),
        (cube_cx + cw//2, cube_cy + ch//2)
    ], fill=(226, 232, 240), outline=(148, 163, 184), width=1)
    
    # Cube top face
    draw.polygon([
        (cube_cx - cw//2, cube_cy - ch//2),
        (cube_cx - cw//2 + cdep_x, cube_cy - ch//2 + cdep_y),
        (cube_cx + cw//2 + cdep_x, cube_cy - ch//2 + cdep_y),
        (cube_cx + cw//2, cube_cy - ch//2)
    ], fill=(255, 255, 255), outline=(203, 213, 225), width=1)
    
    # Cube front face (White with colored icon / number)
    draw.polygon([
        (cube_cx - cw//2, cube_cy - ch//2),
        (cube_cx + cw//2, cube_cy - ch//2),
        (cube_cx + cw//2, cube_cy + ch//2),
        (cube_cx - cw//2, cube_cy + ch//2)
    ], fill=(255, 255, 255), outline=color, width=2)
    
    # Text on cube (01, 02, 03, 04, 05)
    cnum_str = f"0{i+1}"
    c_bbox = draw.textbbox((0, 0), cnum_str, font=font_cube_num)
    c_tw = c_bbox[2] - c_bbox[0]
    draw.text((cube_cx - c_tw//2, cube_cy - 12), cnum_str, fill=color, font=font_cube_num)
    
    # Connect dotted line from card to stair
    card_conn_y = start_card_y + i * (card_h + gap) + card_h // 2
    card_conn_x = card_x + card_w
    stair_dot_x = cube_cx - cw//2 - 10
    stair_dot_y = cube_cy
    
    # Draw dashed connecting line
    mid_x = (card_conn_x + stair_dot_x) // 2
    draw.line([(card_conn_x, card_conn_y), (mid_x, card_conn_y)], fill=color, width=2)
    draw.line([(mid_x, card_conn_y), (mid_x, stair_dot_y)], fill=color, width=2)
    draw.line([(mid_x, stair_dot_y), (stair_dot_x, stair_dot_y)], fill=color, width=2)
    draw.ellipse([stair_dot_x - 4, stair_dot_y - 4, stair_dot_x + 4, stair_dot_y + 4], fill=color)

# Footer
foot_y = H - margin - 35
draw.line([(head_x, foot_y - 10), (W - head_x, foot_y - 10)], fill=(241, 245, 249), width=1)
draw.text((head_x, foot_y), "V.E.R.D.A.N.T. 5-Tier Impact & Strategic Value Ladder · Startup Buildathon India 2026", fill=(100, 116, 139), font=font_sub)

status_txt = "Certified ROI: 99.5% MTTD · 84.9% Tokens · 99.7% Energy Reduction"
bbox = draw.textbbox((0, 0), status_txt, font=font_code)
tw = bbox[2] - bbox[0]
draw.text((W - head_x - tw, foot_y), status_txt, fill=(16, 185, 129), font=font_code)

# Save image
out_buildathon = os.path.normpath(r"C:\Users\Dhairya\Desktop\Active\Buildathon\stair_impacts_benefits_slide.png")
out_desktop = os.path.normpath(r"C:\Users\Dhairya\Desktop\stair_impacts_benefits_slide.png")
img.save(out_buildathon, format="PNG")
img.save(out_desktop, format="PNG")

print(f"SUCCESS: Generated Stair Impacts & Benefits Slide at:\n  - {out_buildathon}\n  - {out_desktop}")
