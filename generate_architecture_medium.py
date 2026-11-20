"""
V.E.R.D.A.N.T. Solution Architecture - Medium Detail & High-Visual Design
Produces a high-resolution 1920x1080 executive presentation slide with:
- 3D shaded stepping stones along the winding serpentine pathway
- Custom vector-rendered visual icons for each milestone
- Balanced "medium detail" technical text (punchy, highly readable, structured)
- Modern enterprise SaaS aesthetic (soft shadows, pill tags, clean badges)
"""
import os
import math
from PIL import Image, ImageDraw, ImageFont

W, H = 1920, 1080
img = Image.new("RGBA", (W, H), (245, 247, 250, 255)) # Soft executive canvas background
draw = ImageDraw.Draw(img)

# Typography
font_title = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 38)
font_sub = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 16)
font_step_title = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 20)
font_step_role = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 12)
font_body = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 13)
font_body_b = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 13)
font_stone_num = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 32)
font_badge = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 12)
font_tag = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 11)
font_footer = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 12)
font_code = ImageFont.truetype("C:/Windows/Fonts/consola.ttf", 11)

# 1. Main Slide Outer Card (Rounded border & soft drop shadow)
c_margin = 35
# Drop shadow simulation
for offset in range(6, 0, -1):
    alpha = int(12 * (7 - offset))
    draw.rounded_rectangle(
        [c_margin - offset, c_margin - offset, W - c_margin + offset, H - c_margin + offset],
        radius=28 + offset,
        outline=(220, 226, 235, alpha),
        width=1
    )
draw.rounded_rectangle([c_margin, c_margin, W - c_margin, H - c_margin], radius=26, fill=(255, 255, 255), outline=(226, 232, 240), width=2)

# 2. Header Section
head_x, head_y = 80, 70

# Draw Stylized 'V' Logo Icon
draw.polygon([
    (head_x, head_y + 4),
    (head_x + 14, head_y + 4),
    (head_x + 22, head_y + 36),
    (head_x + 30, head_y + 4),
    (head_x + 44, head_y + 4),
    (head_x + 22, head_y + 44)
], fill=(15, 23, 42))

draw.text((head_x + 58, head_y - 6), "Solution Architecture For V.E.R.D.A.N.T.", fill=(15, 23, 42), font=font_title)
draw.text((head_x + 60, head_y + 42), "Visual Entropy & Runtime Distillation for Autonomous Net-Reduction Testing · End-to-End Execution Flow", fill=(100, 116, 139), font=font_sub)

# Right Header Badges
rb_y = head_y + 4
b_build_w = 265
b_build_x = W - c_margin - b_build_w - 50
draw.rounded_rectangle([b_build_x, rb_y, b_build_x + b_build_w, rb_y + 36], radius=18, fill=(240, 253, 244), outline=(187, 247, 208), width=1)
draw.text((b_build_x + 18, rb_y + 9), "Google Cloud & DeepMind 2026", fill=(21, 128, 61), font=font_badge)

b_live_w = 175
b_live_x = b_build_x - b_live_w - 14
draw.rounded_rectangle([b_live_x, rb_y, b_live_x + b_live_w, rb_y + 36], radius=18, fill=(239, 246, 255), outline=(191, 219, 254), width=1)
draw.text((b_live_x + 16, rb_y + 9), "● Live Engine Verified", fill=(29, 78, 216), font=font_badge)

# Subtle header divider
draw.line([(head_x, head_y + 78), (W - head_x, head_y + 78)], fill=(241, 245, 249), width=1)

# 3. 3D Stepping Stone Renderer
SW, SH = 100, 72

def draw_3d_stone(x, y, top_color, side_color, label="", shadow=True):
    # Base shadow
    if shadow:
        draw.rounded_rectangle([x - SW//2 + 4, y - SH//2 + 10, x + SW//2 + 4, y + SH//2 + 14], radius=14, fill=(218, 225, 235))
    # 3D side extrusion
    draw.rounded_rectangle([x - SW//2, y - SH//2 + 6, x + SW//2, y + SH//2 + 6], radius=14, fill=side_color)
    # 3D top surface
    draw.rounded_rectangle([x - SW//2, y - SH//2, x + SW//2, y + SH//2], radius=14, fill=top_color)
    # Highlight reflection on top edge
    draw.line([(x - SW//2 + 14, y - SH//2 + 2), (x + SW//2 - 14, y - SH//2 + 2)], fill=(255, 255, 255, 120), width=2)
    # Number label
    if label:
        bbox = draw.textbbox((0, 0), label, font=font_stone_num)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
        draw.text((x - tw//2, y - th//2 - 3), label, fill=(255, 255, 255), font=font_stone_num)

# Neutral connector colors
N_TOP = (203, 213, 225)
N_SIDE = (148, 163, 184)
N_LIGHT_TOP = (226, 232, 240)
N_LIGHT_SIDE = (203, 213, 225)

# Milestone Colors (Top & 3D Extrusion Side)
M_COLORS = {
    "01": ((15, 118, 110), (19, 78, 74)),    # Teal
    "02": ((14, 116, 144), (21, 94, 117)),   # Cyan
    "03": ((180, 83, 9), (120, 53, 15)),     # Amber / Bronze
    "04": ((29, 78, 216), (30, 58, 138)),    # Royal Blue
    "05": ((133, 77, 14), (85, 45, 5))       # Earth Gold
}

# Winding Pathway Coordinates (Matching the reference serpentine path)
# Entry
draw_3d_stone(200, 730, N_LIGHT_TOP, N_LIGHT_SIDE)
draw_3d_stone(290, 730, N_TOP, N_SIDE)

# 01 Ingest
draw_3d_stone(385, 730, M_COLORS["01"][0], M_COLORS["01"][1], label="01")

# Rise to 02
draw_3d_stone(480, 695, N_TOP, N_SIDE)
draw_3d_stone(495, 605, N_TOP, N_SIDE)
draw_3d_stone(505, 515, N_TOP, N_SIDE)
draw_3d_stone(550, 435, N_TOP, N_SIDE)
draw_3d_stone(630, 395, N_TOP, N_SIDE)

# 02 Analyze
draw_3d_stone(720, 395, M_COLORS["02"][0], M_COLORS["02"][1], label="02")

# 03 Arbitrate
draw_3d_stone(825, 395, M_COLORS["03"][0], M_COLORS["03"][1], label="03")

# Downward curve to 04
draw_3d_stone(920, 435, N_TOP, N_SIDE)
draw_3d_stone(955, 520, N_TOP, N_SIDE)
draw_3d_stone(990, 610, N_TOP, N_SIDE)
draw_3d_stone(1045, 690, N_TOP, N_SIDE)
draw_3d_stone(1135, 730, N_TOP, N_SIDE)

# 04 Sandbox Replay
draw_3d_stone(1235, 730, M_COLORS["04"][0], M_COLORS["04"][1], label="04")

# Rise to 05
draw_3d_stone(1335, 685, N_TOP, N_SIDE)
draw_3d_stone(1385, 595, N_TOP, N_SIDE)
draw_3d_stone(1405, 505, N_TOP, N_SIDE)

# 05 Green PR
draw_3d_stone(1405, 400, M_COLORS["05"][0], M_COLORS["05"][1], label="05")

# Draw Curved Flow Guide Dots along stones
dots = [
    (150, 730), (200, 730), (290, 730), (385, 730),
    (480, 695), (495, 605), (505, 515), (550, 435), (630, 395), (720, 395),
    (825, 395), (920, 435), (955, 520), (990, 610), (1045, 690), (1135, 730), (1235, 730),
    (1335, 685), (1385, 595), (1405, 505), (1405, 400), (1485, 400)
]
for i in range(len(dots) - 1):
    p1, p2 = dots[i], dots[i+1]
    # Subtle dashed flow line
    draw.line([p1, p2], fill=(226, 232, 240), width=1)

# Input Entry Indicator
draw.polygon([(145, 730), (135, 723), (135, 737)], fill=(15, 23, 42))
draw.line([(85, 730), (135, 730)], fill=(15, 23, 42), width=3)
draw.text((85, 695), "INGESTION STREAM", fill=(15, 23, 42), font=font_step_role)
draw.text((85, 742), "MP4 · HAR · Logs · AST", fill=(100, 116, 139), font=font_code)

# 4. Custom Vector Visual Icons for each Step

def draw_icon(x, y, icon_type, color):
    # Circular Icon Container
    r = 26
    draw.ellipse([x - r, y - r, x + r, y + r], fill=(255, 255, 255), outline=color, width=2)
    # Background soft tint
    draw.ellipse([x - r + 3, y - r + 3, x + r - 3, y + r - 3], fill=(color[0], color[1], color[2], 25))
    
    if icon_type == "shield":
        # Shield with funnel/filter
        draw.polygon([(x, y - 12), (x + 11, y - 7), (x + 9, y + 5), (x, y + 13), (x - 9, y + 5), (x - 11, y - 7)], fill=color)
        draw.line([(x - 5, y - 4), (x + 5, y - 4)], fill=(255, 255, 255), width=2)
        draw.line([(x - 3, y), (x + 3, y)], fill=(255, 255, 255), width=2)
        draw.line([(x, y + 3), (x, y + 7)], fill=(255, 255, 255), width=2)
        
    elif icon_type == "ai":
        # Neural brain / nodes
        draw.ellipse([x - 10, y - 8, x - 4, y - 2], fill=color)
        draw.ellipse([x + 4, y - 8, x + 10, y - 2], fill=color)
        draw.ellipse([x - 3, y + 3, x + 3, y + 9], fill=color)
        draw.line([(x - 7, y - 5), (x + 7, y - 5)], fill=color, width=2)
        draw.line([(x - 7, y - 5), (x, y + 6)], fill=color, width=2)
        draw.line([(x + 7, y - 5), (x, y + 6)], fill=color, width=2)
        draw.line([(x, y - 12), (x, y - 6)], fill=color, width=2)
        
    elif icon_type == "scales":
        # Decision scales of balance
        draw.line([(x, y - 10), (x, y + 10)], fill=color, width=2) # Pillar
        draw.line([(x - 11, y - 6), (x + 11, y - 6)], fill=color, width=2) # Crossbar
        draw.polygon([(x - 12, y), (x - 6, y), (x - 9, y + 6)], fill=color) # Left pan
        draw.polygon([(x + 6, y), (x + 12, y), (x + 9, y + 6)], fill=color) # Right pan
        draw.line([(x - 6, y + 10), (x + 6, y + 10)], fill=color, width=2) # Base
        
    elif icon_type == "sandbox":
        # Docker container / terminal replay box
        draw.rectangle([x - 11, y - 8, x + 11, y + 8], outline=color, width=2)
        draw.polygon([(x - 3, y - 4), (x + 4, y), (x - 3, y + 4)], fill=color) # Play triangle
        
    elif icon_type == "eco":
        # Eco leaf with git branch
        draw.ellipse([x - 8, y - 10, x + 8, y + 6], fill=color)
        draw.line([(x - 8, y + 6), (x + 8, y - 10)], fill=(255, 255, 255), width=2) # Leaf vein
        draw.line([(x, y + 6), (x, y + 12)], fill=color, width=2) # Stem
        draw.ellipse([x + 2, y + 9, x + 6, y + 13], fill=color) # Git commit node

# 5. Medium-Detail Milestone Presentation Cards

def draw_medium_card(x, y, w, h, stage_num, title, subtitle, badge_txt, bullets, icon_type, color):
    # Card outer shadow
    draw.rounded_rectangle([x + 2, y + 3, x + w + 2, y + h + 3], radius=16, fill=(235, 240, 246))
    # Card body
    draw.rounded_rectangle([x, y, x + w, y + h], radius=16, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    
    # Header strip with color accent
    draw.rounded_rectangle([x, y, x + w, y + 40], radius=16, fill=(248, 250, 252))
    draw.rectangle([x, y + 24, x + w, y + 40], fill=(248, 250, 252))
    draw.line([(x, y + 40), (x + w, y + 40)], fill=(235, 240, 246), width=1)
    
    # Left colored vertical accent tab
    draw.rounded_rectangle([x, y, x + 5, y + h], radius=3, fill=color)
    
    # Title & Badge
    draw.text((x + 16, y + 10), title, fill=(15, 23, 42), font=font_step_title)
    
    # Subtitle / Architectural Role
    draw.text((x + 16, y + 48), subtitle.upper(), fill=color, font=font_step_role)
    
    # Pill Badge (Metric / Guarantee)
    bbox = draw.textbbox((0, 0), badge_txt, font=font_tag)
    bw = bbox[2] - bbox[0] + 16
    draw.rounded_rectangle([x + 16, y + 68, x + 16 + bw, y + 88], radius=6, fill=(241, 245, 249), outline=(226, 232, 240), width=1)
    draw.text((x + 24, y + 71), badge_txt, fill=(51, 65, 85), font=font_tag)
    
    # 3 Crisp, High-Impact Bullets
    by = y + 100
    for b_lead, b_rest in bullets:
        # Bullet marker
        draw.ellipse([x + 16, by + 4, x + 22, by + 10], fill=color)
        draw.text((x + 28, by), b_lead, fill=(15, 23, 42), font=font_body_b)
        lead_w = draw.textbbox((0, 0), b_lead, font=font_body_b)[2] - draw.textbbox((0, 0), b_lead, font=font_body_b)[0]
        draw.text((x + 30 + lead_w, by), b_rest, fill=(71, 85, 105), font=font_body)
        by += 24

# CARD 01: ContextPrism (Bottom-Left)
draw_icon(220, 805, "shield", M_COLORS["01"][0])
draw_medium_card(
    x=60, y=835, w=385, h=180,
    stage_num="01",
    title="01 · Context Ingestion",
    subtitle="Zero-Trust Distillation & PII Scrub",
    badge_txt="84.9% TOKEN REDUCTION · ZERO PII LEAK",
    bullets=[
        ("OpenCV 4.10 Keyframes: ", "Extracts active delta frames, dropping idle video."),
        ("Regex PII Perimeter: ", "Scrubs Bearer tokens, passwords & user secrets."),
        ("AST Skeletonizer: ", "Retains interface signatures, stripping body bloat.")
    ],
    icon_type="shield",
    color=M_COLORS["01"][0]
)

# CARD 02: ApexTrace (Top-Left / Center)
draw_icon(560, 155, "ai", M_COLORS["02"][0])
draw_medium_card(
    x=410, y=185, w=390, h=180,
    stage_num="02",
    title="02 · Dual-Engine Analysis",
    subtitle="Semantic AI + Mathematical Sentinel",
    badge_txt="GEMINI 3.1 FLASH-LITE + SSIM MATRIX",
    bullets=[
        ("Engine A (Semantic): ", "Gemini 3.1 reasons across AST & HTTP timeline."),
        ("Engine B (Math): ", "SSIM covariance (<0.92) & pixel-delta sentinel."),
        ("Zero Hallucination: ", "Correlates DOM repaints against failure anchors.")
    ],
    icon_type="ai",
    color=M_COLORS["02"][0]
)

# CARD 03: Consensus Arbiter (Top-Right / Center)
draw_icon(970, 155, "scales", M_COLORS["03"][0])
draw_medium_card(
    x=825, y=185, w=395, h=180,
    stage_num="03",
    title="03 · Consensus Arbiter",
    subtitle="Deterministic 3-Tier Precedence",
    badge_txt="100% FALSE-POSITIVE REJECTION",
    bullets=[
        ("Tier 1 (Deterministic): ", "HTTP 4xx/5xx & console errors rule over visual."),
        ("Tier 2 (Silent Freeze): ", "Flags click actions with 0% DOM pixel repaint."),
        ("Bayesian Scoring: ", "Outputs calibrated confidence score (e.g. 94.8%).")
    ],
    icon_type="scales",
    color=M_COLORS["03"][0]
)

# CARD 04: Replay Shield (Bottom-Right)
draw_icon(1060, 805, "sandbox", M_COLORS["04"][0])
draw_medium_card(
    x=900, y=835, w=405, h=180,
    stage_num="04",
    title="04 · Replay Shield Sandbox",
    subtitle="Hermetic Playwright Verification",
    badge_txt="CLOSED-LOOP TDD (RED → GREEN)",
    bullets=[
        ("Playwright Synthesizer: ", "Generates robust role-based executable tests."),
        ("Docker Container: ", "Isolated non-root replay with locked network egress."),
        ("TDD Proving Loop: ", "Verifies test fails on bug, passes on AST patch.")
    ],
    icon_type="sandbox",
    color=M_COLORS["04"][0]
)

# CARD 05: VERDE-Hydra Telemetry & GitHub PR (Far Right)
draw_icon(1520, 155, "eco", M_COLORS["05"][0])
draw_medium_card(
    x=1345, y=185, w=485, h=245,
    stage_num="05",
    title="05 · Green Telemetry & PR",
    subtitle="ESG Carbon Audit & GitHub Dispatch",
    badge_txt="99.7% ENERGY SAVINGS · PUE 1.10 · WUE 1.80",
    bullets=[
        ("Google Cloud Telemetry: ", "Audited with PUE 1.10 & 1.80 L/kWh water metric."),
        ("Energy Comparison: ", "Autonomous triage (0.28 Wh) vs manual engineer (90 Wh)."),
        ("Automated GitHub PR: ", "Dispatches reviewer-ready PR with patch diff & test."),
        ("Evidence Ledger: ", "Includes cryptographic reproduction audit trail.")
    ],
    icon_type="eco",
    color=M_COLORS["05"][0]
)

# Bottom-Right Companion Box: Enterprise Architectural Invariants
eb_x, eb_y, eb_w, eb_h = 1345, 455, 485, 230
draw.rounded_rectangle([eb_x + 2, eb_y + 3, eb_x + eb_w + 2, eb_y + eb_h + 3], radius=16, fill=(235, 240, 246))
draw.rounded_rectangle([eb_x, eb_y, eb_x + eb_w, eb_y + eb_h], radius=16, fill=(255, 255, 255), outline=(226, 232, 240), width=1)

# Header
draw.rounded_rectangle([eb_x, eb_y, eb_x + eb_w, eb_y + 36], radius=16, fill=(248, 250, 252))
draw.rectangle([eb_x, eb_y + 20, eb_x + eb_w, eb_y + 36], fill=(248, 250, 252))
draw.line([(eb_x, eb_y + 36), (eb_x + eb_w, eb_y + 36)], fill=(235, 240, 246), width=1)
draw.text((eb_x + 16, eb_y + 9), "Architectural Invariants & Guarantees", fill=(15, 23, 42), font=font_step_title)

# Content items
invariants = [
    ("Zero Context Poisoning: ", "Regex masks all auth credentials prior to LLM."),
    ("Hermetic Execution: ", "Ephemeral Docker sandboxes destroyed post-replay."),
    ("Dual-Engine Consensus: ", "Deterministic SSIM vetoes AI visual hallucinations."),
    ("Automated CI/CD Ready: ", "Native GitHub draft PR payload with Playwright test.")
]
iy = eb_y + 48
for inv_lead, inv_body in invariants:
    draw.text((eb_x + 16, iy), "✔", fill=(16, 185, 129), font=font_body_b)
    draw.text((eb_x + 34, iy), inv_lead, fill=(15, 23, 42), font=font_body_b)
    lead_w = draw.textbbox((0, 0), inv_lead, font=font_body_b)[2] - draw.textbbox((0, 0), inv_lead, font=font_body_b)[0]
    draw.text((eb_x + 36 + lead_w, iy), inv_body, fill=(71, 85, 105), font=font_body)
    iy += 24

# Footer Bar
foot_y = H - c_margin - 35
draw.line([(head_x, foot_y - 10), (W - head_x, foot_y - 10)], fill=(241, 245, 249), width=1)
draw.text((head_x, foot_y), "V.E.R.D.A.N.T. Solution Architecture Blueprint · Startup Buildathon India 2026", fill=(100, 116, 139), font=font_footer)

stat_txt = "Pipeline Status: Fully Operational on Port 8000"
bbox = draw.textbbox((0, 0), stat_txt, font=font_code)
tw = bbox[2] - bbox[0]
draw.text((W - head_x - tw, foot_y), stat_txt, fill=(16, 185, 129), font=font_code)

# Save high-res outputs
out_buildathon = "C:/Users/Dhairya/Desktop/Active/Buildathon/solution_architecture_verdant_medium.png"
out_desktop = "C:/Users/Dhairya/Desktop/solution_architecture_verdant_medium.png"
img.save(out_buildathon, "PNG")
img.save(out_desktop, "PNG")

print(f"Generated Medium-Detail Solution Architecture Slide:\n  - {out_buildathon}\n  - {out_desktop}")
