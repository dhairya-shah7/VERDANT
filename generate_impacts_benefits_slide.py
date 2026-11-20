"""
Impacts & Benefits Slide Generator for V.E.R.D.A.N.T.
Creates a high-resolution 1920x1080 presentation slide graphic for Slide 8.
Structure:
- Clean white canvas with soft modern grid
- 2 Equal Vertical Halves:
  * Left Half: MEASURABLE ENGINEERING IMPACTS (with visual gauges & comparison meters)
  * Right Half: STRATEGIC ENTERPRISE BENEFITS (with modern feature cards & icons)
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
font_col_header = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 22)
font_col_sub = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 12)
font_card_title = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 18)
font_card_desc = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 13)
font_big_num = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 32)
font_metric_lbl = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 11)
font_code = ImageFont.truetype("C:/Windows/Fonts/consola.ttf", 11)
font_code_b = ImageFont.truetype("C:/Windows/Fonts/consolab.ttf", 11)
font_tag = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 10)
font_badge = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 12)

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

draw.text((head_x + 60, head_y - 6), "Impacts & Strategic Benefits", fill=(15, 23, 42), font=font_title)
draw.text((head_x + 62, head_y + 40), "Measurable Engineering Triage Performance vs Enterprise & Developer Value · V.E.R.D.A.N.T.", fill=(100, 116, 139), font=font_sub)

# Top Right Badges
rb_y = head_y + 2
b1_w = 265
b1_x = W - margin - b1_w - 50
draw.rounded_rectangle([b1_x, rb_y, b1_x + b1_w, rb_y + 36], radius=18, fill=(240, 253, 244), outline=(187, 247, 208), width=1)
draw.text((b1_x + 18, rb_y + 9), "Google Cloud & DeepMind 2026", fill=(21, 128, 61), font=font_badge)

b2_w = 195
b2_x = b1_x - b2_w - 14
draw.rounded_rectangle([b2_x, rb_y, b2_x + b2_w, rb_y + 36], radius=18, fill=(239, 246, 255), outline=(191, 219, 254), width=1)
draw.text((b2_x + 16, rb_y + 9), "● Verified ROI & Value", fill=(29, 78, 216), font=font_badge)

draw.line([(head_x, head_y + 78), (W - head_x, head_y + 78)], fill=(241, 245, 249), width=1)

# 4. Vertical Split Columns Layout
# Working area: y from 145 to 990 (height = 845)
# Width = W - 2*head_x = 1790
# Two columns of width ~875 each, gap ~40
col_w = 875
col_gap = 40
col_h = 825
col_y = 150

left_x = head_x
right_x = head_x + col_w + col_gap

# -------------------------------------------------------------
# LEFT VERTICAL HALF: MEASURABLE ENGINEERING IMPACTS
# -------------------------------------------------------------
# Column Container
draw.rounded_rectangle([left_x + 3, col_y + 4, left_x + col_w + 3, col_y + col_h + 4], radius=20, fill=(235, 240, 246))
draw.rounded_rectangle([left_x, col_y, left_x + col_w, col_y + col_h], radius=20, fill=(255, 255, 255), outline=(226, 232, 240), width=1)

# Column Header
draw.rounded_rectangle([left_x, col_y, left_x + col_w, col_y + 58], radius=20, fill=(240, 253, 250))
draw.rectangle([left_x, col_y + 35, left_x + col_w, col_y + 58], fill=(240, 253, 250))
draw.line([(left_x, col_y + 58), (left_x + col_w, col_y + 58)], fill=(204, 251, 241), width=1)

# Left Column Accent Bar
draw.rounded_rectangle([left_x + 20, col_y + 14, left_x + 26, col_y + 44], radius=3, fill=(13, 148, 136))
draw.text((left_x + 36, col_y + 12), "MEASURABLE ENGINEERING IMPACTS", fill=(15, 23, 42), font=font_col_header)
draw.text((left_x + 38, col_y + 38), "Quantifiable benchmarks verified through automated test runs and mathematical models", fill=(13, 148, 136), font=font_col_sub)

# 4 Big Visual Metric Cards inside Left Column
card_w_inner = col_w - 40
card_h_inner = 170
card_spacing = 18
start_y = col_y + 75

# Impact 1: 99.5% Faster Triage (Time to Diagnose)
c1_y = start_y
draw.rounded_rectangle([left_x + 20, c1_y, left_x + 20 + card_w_inner, c1_y + card_h_inner], radius=14, fill=(248, 250, 252), outline=(226, 232, 240), width=1)
# Circular Progress Gauge on left of card
gauge_cx, gauge_cy = left_x + 95, c1_y + card_h_inner // 2
gr = 48
draw.ellipse([gauge_cx - gr, gauge_cy - gr, gauge_cx + gr, gauge_cy + gr], outline=(226, 232, 240), width=10)
draw.arc([gauge_cx - gr, gauge_cy - gr, gauge_cx + gr, gauge_cy + gr], start=-90, end=268, fill=(13, 148, 136), width=10) # 99.5%
draw.text((gauge_cx - 36, gauge_cy - 16), "99.5%", fill=(15, 23, 42), font=font_card_title)
draw.text((gauge_cx - 26, gauge_cy + 6), "FASTER", fill=(13, 148, 136), font=font_tag)

# Card Text
tx = left_x + 175
draw.text((tx, c1_y + 18), "MEAN TIME TO DIAGNOSE (MTTD)", fill=(100, 116, 139), font=font_tag)
draw.text((tx, c1_y + 36), "12.0 Seconds vs 45.0 Minutes Manual", fill=(15, 23, 42), font=font_card_title)
draw.text((tx, c1_y + 68), "• Autonomous AI-driven correlation cuts triage time from ~45 minutes of manual", fill=(71, 85, 105), font=font_card_desc)
draw.text((tx, c1_y + 88), "  developer reproduction down to 12 seconds automated execution.", fill=(71, 85, 105), font=font_card_desc)
# Comparison Bar
draw.rounded_rectangle([tx, c1_y + 118, tx + 450, c1_y + 138], radius=6, fill=(226, 232, 240))
draw.rounded_rectangle([tx, c1_y + 118, tx + 20, c1_y + 138], radius=6, fill=(13, 148, 136)) # only 12s
draw.text((tx + 28, c1_y + 121), "V.E.R.D.A.N.T. (12s)", fill=(13, 148, 136), font=font_code_b)
draw.text((tx + 270, c1_y + 121), "Manual Engineering (45m)", fill=(100, 116, 139), font=font_code)

# Impact 2: 99.7% Energy & Water Reduction (Green ESG)
c2_y = c1_y + card_h_inner + card_spacing
draw.rounded_rectangle([left_x + 20, c2_y, left_x + 20 + card_w_inner, c2_y + card_h_inner], radius=14, fill=(248, 250, 252), outline=(226, 232, 240), width=1)
# Circular Progress Gauge
g2_cx, g2_cy = left_x + 95, c2_y + card_h_inner // 2
draw.ellipse([g2_cx - gr, g2_cy - gr, g2_cx + gr, g2_cy + gr], outline=(226, 232, 240), width=10)
draw.arc([g2_cx - gr, g2_cy - gr, g2_cx + gr, g2_cy + gr], start=-90, end=269, fill=(16, 185, 129), width=10) # 99.7%
draw.text((g2_cx - 36, g2_cy - 16), "99.7%", fill=(15, 23, 42), font=font_card_title)
draw.text((g2_cx - 24, g2_cy + 6), "SAVED", fill=(16, 185, 129), font=font_tag)

draw.text((tx, c2_y + 18), "GOOGLE CLOUD ESG GREEN COMPUTE", fill=(100, 116, 139), font=font_tag)
draw.text((tx, c2_y + 36), "0.28 Wh Energy & 0.50 ml H2O Consumed", fill=(15, 23, 42), font=font_card_title)
draw.text((tx, c2_y + 68), "• Audited with Google Cloud PUE = 1.10 and global cooling WUE = 1.80 L/kWh.", fill=(71, 85, 105), font=font_card_desc)
draw.text((tx, c2_y + 88), "• Replaces high-draw multi-agent polling with sub-second event-driven triggers.", fill=(71, 85, 105), font=font_card_desc)

draw.rounded_rectangle([tx, c2_y + 118, tx + 450, c2_y + 138], radius=6, fill=(240, 253, 244), outline=(187, 247, 208), width=1)
draw.text((tx + 14, c2_y + 121), "ECO LEDGER: 0.28 Wh vs 90.0 Wh manual triage | -99.7% carbon", fill=(21, 128, 61), font=font_code_b)

# Impact 3: 84.9% Token Reduction (AST Skeletonizer)
c3_y = c2_y + card_h_inner + card_spacing
draw.rounded_rectangle([left_x + 20, c3_y, left_x + 20 + card_w_inner, c3_y + card_h_inner], radius=14, fill=(248, 250, 252), outline=(226, 232, 240), width=1)
# Circular Progress Gauge
g3_cx, g3_cy = left_x + 95, c3_y + card_h_inner // 2
draw.ellipse([g3_cx - gr, g3_cy - gr, g3_cx + gr, g3_cy + gr], outline=(226, 232, 240), width=10)
draw.arc([g3_cx - gr, g3_cy - gr, g3_cx + gr, g3_cy + gr], start=-90, end=216, fill=(66, 133, 244), width=10) # 84.9%
draw.text((g3_cx - 36, g3_cy - 16), "84.9%", fill=(15, 23, 42), font=font_card_title)
draw.text((g3_cx - 30, g3_cy + 6), "PRUNED", fill=(66, 133, 244), font=font_tag)

draw.text((tx, c3_y + 18), "CONTEXT WINDOW DISTILLATION", fill=(100, 116, 139), font=font_tag)
draw.text((tx, c3_y + 36), "119 Tokens ➔ 45 Tokens (AST Interface Skel)", fill=(15, 23, 42), font=font_card_title)
draw.text((tx, c3_y + 68), "• Strips bloated function implementation bodies, retaining strict type signatures.", fill=(71, 85, 105), font=font_card_desc)
draw.text((tx, c3_y + 88), "• Completely prevents 'Lost-in-the-Middle' degradation & slashes inference cost.", fill=(71, 85, 105), font=font_card_desc)

draw.rounded_rectangle([tx, c3_y + 118, tx + 450, c3_y + 138], radius=6, fill=(239, 246, 255), outline=(191, 219, 254), width=1)
draw.text((tx + 14, c3_y + 121), "TOKEN EFFICIENCY: Zero context poisoning | Sub-2.4s TTFT", fill=(29, 78, 216), font=font_code_b)

# Impact 4: 100% False-Positive Rejection (Consensus Arbiter)
c4_y = c3_y + card_h_inner + card_spacing
draw.rounded_rectangle([left_x + 20, c4_y, left_x + 20 + card_w_inner, c4_y + card_h_inner], radius=14, fill=(248, 250, 252), outline=(226, 232, 240), width=1)
# Circular Progress Gauge
g4_cx, g4_cy = left_x + 95, c4_y + card_h_inner // 2
draw.ellipse([g4_cx - gr, g4_cy - gr, g4_cx + gr, g4_cy + gr], outline=(226, 232, 240), width=10)
draw.arc([g4_cx - gr, g4_cy - gr, g4_cx + gr, g4_cy + gr], start=-90, end=270, fill=(217, 119, 6), width=10) # 100%
draw.text((g4_cx - 28, g4_cy - 16), "100%", fill=(15, 23, 42), font=font_card_title)
draw.text((g4_cx - 26, g4_cy + 6), "GATED", fill=(217, 119, 6), font=font_tag)

draw.text((tx, c4_y + 18), "DETERMINISTIC CONSENSUS ARBITER", fill=(100, 116, 139), font=font_tag)
draw.text((tx, c4_y + 36), "Zero False Positives via 3-Tier Precedence", fill=(15, 23, 42), font=font_card_title)
draw.text((tx, c4_y + 68), "• Tier 1 (Deterministic Network/Console) overrides transient visual noise.", fill=(71, 85, 105), font=font_card_desc)
draw.text((tx, c4_y + 88), "• Flags silent UI freeze when user click triggers 0.00% DOM pixel repaints.", fill=(71, 85, 105), font=font_card_desc)

draw.rounded_rectangle([tx, c4_y + 118, tx + 450, c4_y + 138], radius=6, fill=(255, 251, 235), outline=(254, 215, 170), width=1)
draw.text((tx + 14, c4_y + 121), "BAYESIAN CONFIDENCE: 94.8% calibrated score attached to PR", fill=(180, 83, 9), font=font_code_b)

# -------------------------------------------------------------
# RIGHT VERTICAL HALF: STRATEGIC ENTERPRISE BENEFITS
# -------------------------------------------------------------
# Column Container
draw.rounded_rectangle([right_x + 3, col_y + 4, right_x + col_w + 3, col_y + col_h + 4], radius=20, fill=(235, 240, 246))
draw.rounded_rectangle([right_x, col_y, right_x + col_w, col_y + col_h], radius=20, fill=(255, 255, 255), outline=(226, 232, 240), width=1)

# Column Header
draw.rounded_rectangle([right_x, col_y, right_x + col_w, col_y + 58], radius=20, fill=(239, 246, 255))
draw.rectangle([right_x, col_y + 35, right_x + col_w, col_y + 58], fill=(239, 246, 255))
draw.line([(right_x, col_y + 58), (right_x + col_w, col_y + 58)], fill=(191, 219, 254), width=1)

# Right Column Accent Bar
draw.rounded_rectangle([right_x + 20, col_y + 14, right_x + 26, col_y + 44], radius=3, fill=(29, 78, 216))
draw.text((right_x + 36, col_y + 12), "STRATEGIC ENTERPRISE BENEFITS", fill=(15, 23, 42), font=font_col_header)
draw.text((right_x + 38, col_y + 38), "High-value developer experience, security compliance, and organizational scalability", fill=(29, 78, 216), font=font_col_sub)

# 4 Visual Benefit Cards inside Right Column

def draw_benefit_icon(x, y, icon_type, color):
    r = 30
    draw.ellipse([x - r, y - r, x + r, y + r], fill=(255, 255, 255), outline=color, width=2)
    draw.ellipse([x - r + 3, y - r + 3, x + r - 3, y + r - 3], fill=(color[0], color[1], color[2], 25))
    if icon_type == "shield":
        # Security shield
        draw.polygon([(x, y - 14), (x + 13, y - 8), (x + 11, y + 6), (x, y + 15), (x - 11, y + 6), (x - 13, y - 8)], fill=color)
        draw.line([(x - 5, y), (x + 5, y)], fill=(255, 255, 255), width=2)
        draw.line([(x, y - 5), (x, y + 5)], fill=(255, 255, 255), width=2)
    elif icon_type == "loop":
        # TDD Replay Loop
        draw.arc([x - 14, y - 14, x + 14, y + 14], start=45, end=315, fill=color, width=3)
        draw.polygon([(x + 10, y - 14), (x + 18, y - 8), (x + 10, y - 2)], fill=color)
    elif icon_type == "git":
        # Git branch
        draw.line([(x - 8, y - 12), (x - 8, y + 12)], fill=color, width=3)
        draw.arc([x - 8, y - 4, x + 10, y + 12], start=180, end=270, fill=color, width=3)
        draw.line([(x + 10, y + 4), (x + 10, y + 12)], fill=color, width=3)
        draw.ellipse([x - 11, y - 14, x - 5, y - 8], fill=color)
        draw.ellipse([x - 11, y + 8, x - 5, y + 14], fill=color)
        draw.ellipse([x + 7, y + 8, x + 13, y + 14], fill=color)
    elif icon_type == "cloud":
        # Cloud serverless
        draw.ellipse([x - 12, y - 4, x + 2, y + 10], fill=color)
        draw.ellipse([x - 4, y - 12, x + 12, y + 4], fill=color)
        draw.ellipse([x + 2, y - 4, x + 14, y + 10], fill=color)
        draw.rectangle([x - 8, y + 2, x + 10, y + 10], fill=color)

# Benefit 1: SOC2 & GDPR Zero-Trust Data Boundary
b1_y = start_y
draw.rounded_rectangle([right_x + 20, b1_y, right_x + 20 + card_w_inner, b1_y + card_h_inner], radius=14, fill=(248, 250, 252), outline=(226, 232, 240), width=1)
draw_benefit_icon(right_x + 95, b1_y + card_h_inner // 2, "shield", (29, 78, 216))

rtx = right_x + 175
draw.text((rtx, b1_y + 18), "DATA SECURITY & PRIVACY", fill=(100, 116, 139), font=font_tag)
draw.text((rtx, b1_y + 36), "Zero-Trust SOC2 & GDPR Perimeter", fill=(15, 23, 42), font=font_card_title)
draw.text((rtx, b1_y + 68), "• Multi-pass regex scrubbing sanitizes Authorization headers, Bearer tokens,", fill=(71, 85, 105), font=font_card_desc)
draw.text((rtx, b1_y + 88), "  passwords, and session cookies before payloads leave the ingestion boundary.", fill=(71, 85, 105), font=font_card_desc)

draw.rounded_rectangle([rtx, b1_y + 118, rtx + 450, b1_y + 138], radius=6, fill=(239, 246, 255), outline=(191, 219, 254), width=1)
draw.text((rtx + 14, b1_y + 121), "SECURITY COMPLIANCE: 100% PII isolation | Zero credential leak", fill=(29, 78, 216), font=font_code_b)

# Benefit 2: Hermetic Closed-Loop TDD Verification
b2_y = b1_y + card_h_inner + card_spacing
draw.rounded_rectangle([right_x + 20, b2_y, right_x + 20 + card_w_inner, b2_y + card_h_inner], radius=14, fill=(248, 250, 252), outline=(226, 232, 240), width=1)
draw_benefit_icon(right_x + 95, b2_y + card_h_inner // 2, "loop", (147, 51, 234))

draw.text((rtx, b2_y + 18), "ENGINEERING VERIFICATION", fill=(100, 116, 139), font=font_tag)
draw.text((rtx, b2_y + 36), "Hermetic Closed-Loop TDD Replay", fill=(15, 23, 42), font=font_card_title)
draw.text((rtx, b2_y + 68), "• Synthesizes executable Playwright tests inside isolated Docker sandboxes.", fill=(71, 85, 105), font=font_card_desc)
draw.text((rtx, b2_y + 88), "• Enforces RED (proves bug) then GREEN (proves fix) before any patch is accepted.", fill=(71, 85, 105), font=font_card_desc)

draw.rounded_rectangle([rtx, b2_y + 118, rtx + 450, b2_y + 138], radius=6, fill=(250, 245, 255), outline=(233, 213, 255), width=1)
draw.text((rtx + 14, b2_y + 121), "TDD RIGOR: Zero untested hallucinated code merged to production", fill=(126, 34, 206), font=font_code_b)

# Benefit 3: Zero-Friction Automated GitOps
b3_y = b2_y + card_h_inner + card_spacing
draw.rounded_rectangle([right_x + 20, b3_y, right_x + 20 + card_w_inner, b3_y + card_h_inner], radius=14, fill=(248, 250, 252), outline=(226, 232, 240), width=1)
draw_benefit_icon(right_x + 95, b3_y + card_h_inner // 2, "git", (13, 148, 136))

draw.text((rtx, b3_y + 18), "DEVELOPER PRODUCTIVITY", fill=(100, 116, 139), font=font_tag)
draw.text((rtx, b3_y + 36), "Zero-Friction GitOps PR Dispatch", fill=(15, 23, 42), font=font_card_title)
draw.text((rtx, b3_y + 68), "• Automatically opens a reviewer-ready GitHub Draft PR with patch diff,", fill=(71, 85, 105), font=font_card_desc)
draw.text((rtx, b3_y + 88), "  regression test suite, and cryptographic evidence hashes attached.", fill=(71, 85, 105), font=font_card_desc)

draw.rounded_rectangle([rtx, b3_y + 118, rtx + 450, b3_y + 138], radius=6, fill=(240, 253, 250), outline=(204, 251, 241), width=1)
draw.text((rtx + 14, b3_y + 121), "PR PAYLOAD: One-click merge for senior engineers | Full audit trail", fill=(13, 148, 136), font=font_code_b)

# Benefit 4: Zero-Cost Serverless Cloud Scaling
b4_y = b3_y + card_h_inner + card_spacing
draw.rounded_rectangle([right_x + 20, b4_y, right_x + 20 + card_w_inner, b4_y + card_h_inner], radius=14, fill=(248, 250, 252), outline=(226, 232, 240), width=1)
draw_benefit_icon(right_x + 95, b4_y + card_h_inner // 2, "cloud", (251, 188, 5))

draw.text((rtx, b4_y + 18), "INFRASTRUCTURE SCALABILITY", fill=(100, 116, 139), font=font_tag)
draw.text((rtx, b4_y + 36), "Zero-Cost Serverless Cloud Run Scaling", fill=(15, 23, 42), font=font_card_title)
draw.text((rtx, b4_y + 68), "• Deploys serverlessly on Google Cloud Run with automatic scale-to-zero", fill=(71, 85, 105), font=font_card_desc)
draw.text((rtx, b4_y + 88), "  when idle, completely eliminating continuous standing VM compute costs.", fill=(71, 85, 105), font=font_card_desc)

draw.rounded_rectangle([rtx, b4_y + 118, rtx + 450, b4_y + 138], radius=6, fill=(254, 252, 232), outline=(254, 240, 138), width=1)
draw.text((rtx + 14, b4_y + 121), "ENTERPRISE INFRA: $0 idle expense | Always-Free Tier compatible", fill=(180, 83, 9), font=font_code_b)

# 5. Footer
foot_y = H - margin - 35
draw.line([(head_x, foot_y - 10), (W - head_x, foot_y - 10)], fill=(241, 245, 249), width=1)
draw.text((head_x, foot_y), "V.E.R.D.A.N.T. Executive Impact & Value Ledger · Startup Buildathon India 2026", fill=(100, 116, 139), font=font_sub)

status_txt = "Validated Live on Port 8000 · Ready for City Buildathon Nov 20-21"
bbox = draw.textbbox((0, 0), status_txt, font=font_code_b)
tw = bbox[2] - bbox[0]
draw.text((W - head_x - tw, foot_y), status_txt, fill=(16, 185, 129), font=font_code_b)

# Save Outputs
out_buildathon = os.path.normpath(r"C:\Users\Dhairya\Desktop\Active\Buildathon\impacts_and_benefits_verdant.png")
out_desktop = os.path.normpath(r"C:\Users\Dhairya\Desktop\impacts_and_benefits_verdant.png")
img.save(out_buildathon, format="PNG")
img.save(out_desktop, format="PNG")

print(f"Successfully generated Impacts & Benefits Slide at:\n  - {out_buildathon}\n  - {out_desktop}")
