"""
V.E.R.D.A.N.T. High-Density Solution Architecture Generator
Produces a high-resolution, pixel-perfect 1920x1080 enterprise architecture diagram
following the winding stepping-stone roadmap from the reference design,
enriched with complete data flows, subsystems, mathematical models, and specs.
"""
import os
import math
from PIL import Image, ImageDraw, ImageFont

W, H = 1920, 1080
img = Image.new("RGBA", (W, H), (248, 250, 252, 255)) # Soft slate-50 background
draw = ImageDraw.Draw(img)

# Typography
font_header_title = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 34)
font_header_sub = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 15)
font_card_title = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 16)
font_card_sub = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 12)
font_section_h = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 12)
font_code = ImageFont.truetype("C:/Windows/Fonts/consola.ttf", 11)
font_code_b = ImageFont.truetype("C:/Windows/Fonts/consolab.ttf", 11)
font_stone_num = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 32)
font_badge = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 12)
font_footer = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 12)
font_tag = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 10)

# 1. Main Canvas Card Outline
margin = 25
draw.rounded_rectangle([margin, margin, W - margin, H - margin], radius=20, fill=(255, 255, 255), outline=(226, 232, 240), width=2)

# 2. Header Section
head_x, head_y = 60, 48
# Geometric Logo Icon
draw.polygon([
    (head_x, head_y + 4),
    (head_x + 14, head_y + 4),
    (head_x + 22, head_y + 32),
    (head_x + 30, head_y + 4),
    (head_x + 44, head_y + 4),
    (head_x + 22, head_y + 40)
], fill=(15, 23, 42))

draw.text((head_x + 55, head_y - 4), "Solution Architecture For V.E.R.D.A.N.T.", fill=(15, 23, 42), font=font_header_title)
draw.text((head_x + 57, head_y + 38), "Visual Entropy & Runtime Distillation for Autonomous Net-Reduction Testing · Full End-to-End Enterprise Pipeline", fill=(100, 116, 139), font=font_header_sub)

# Badges on top right
b_y = head_y + 4
b_x2 = W - margin - 50

# Badge 2: Buildathon
b2_w = 260
b2_x = b_x2 - b2_w
draw.rounded_rectangle([b2_x, b_y, b2_x + b2_w, b_y + 34], radius=8, fill=(240, 253, 244), outline=(187, 247, 208), width=1)
draw.text((b2_x + 14, b_y + 8), "Google Cloud & DeepMind Buildathon", fill=(21, 128, 61), font=font_badge)

# Badge 1: Verification status
b1_w = 175
b1_x = b2_x - b1_w - 12
draw.rounded_rectangle([b1_x, b_y, b1_x + b1_w, b_y + 34], radius=8, fill=(239, 246, 255), outline=(191, 219, 254), width=1)
draw.text((b1_x + 14, b_y + 8), "● Live Verified on 8000", fill=(29, 78, 216), font=font_badge)

# Divider under header
draw.line([(head_x, head_y + 72), (W - head_x, head_y + 72)], fill=(241, 245, 249), width=1)

# 3. Stepping Stone Geometry & Helper
BW, BH = 95, 70

def draw_stone(x, y, color=(203, 213, 225), shadow=True, label="", radius=12):
    if shadow:
        draw.rounded_rectangle([x - BW//2 + 3, y - BH//2 + 5, x + BW//2 + 3, y + BH//2 + 5], radius=radius, fill=(226, 232, 240))
    draw.rounded_rectangle([x - BW//2, y - BH//2, x + BW//2, y + BH//2], radius=radius, fill=color)
    if label:
        bbox = draw.textbbox((0, 0), label, font=font_stone_num)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
        draw.text((x - tw//2, y - th//2 - 3), label, fill=(255, 255, 255), font=font_stone_num)

NEUTRAL = (203, 213, 225)
NEUTRAL_LIGHT = (226, 232, 240)

# Colors for 5 Milestone Stages
C01 = (13, 148, 136) # Teal
C02 = (2, 132, 199)  # Cyan / Blue
C03 = (217, 119, 6)  # Amber
C04 = (37, 99, 235)  # Royal Blue
C05 = (180, 83, 9)   # Earth Bronze

# Draw Stones along the Snake Path:
# Path Entrance
draw_stone(190, 715, NEUTRAL_LIGHT)
draw_stone(275, 715, NEUTRAL)
# Milestone 01
draw_stone(360, 715, C01, label="01")

# Rise to 02
draw_stone(445, 680, NEUTRAL)
draw_stone(455, 595, NEUTRAL)
draw_stone(465, 510, NEUTRAL)
draw_stone(510, 435, NEUTRAL)
draw_stone(585, 400, NEUTRAL)
# Milestone 02
draw_stone(670, 400, C02, label="02")

# Milestone 03 (adjacent top)
draw_stone(765, 400, C03, label="03")

# Downward curve from 03 to 04
draw_stone(855, 440, NEUTRAL)
draw_stone(890, 520, NEUTRAL)
draw_stone(925, 605, NEUTRAL)
draw_stone(975, 680, NEUTRAL)
draw_stone(1055, 715, NEUTRAL)
# Milestone 04
draw_stone(1150, 715, C04, label="04")

# Rise to 05
draw_stone(1240, 675, NEUTRAL)
draw_stone(1285, 590, NEUTRAL)
draw_stone(1305, 505, NEUTRAL)
# Milestone 05
draw_stone(1305, 410, C05, label="05")

# Draw Input Arrow on left
draw.line([(70, 715), (135, 715)], fill=(15, 23, 42), width=3)
draw.polygon([(142, 715), (132, 709), (132, 721)], fill=(15, 23, 42))
draw.text((70, 685), "RAW INPUT STREAM", fill=(15, 23, 42), font=font_section_h)
draw.text((70, 728), "MP4 · HAR · Logs · AST", fill=(100, 116, 139), font=font_code)

# 4. Rich Technical Architecture Cards

def draw_tech_card(x, y, w, h, stage_num, title, role, in_spec, core_tech, out_spec, metrics, color):
    # Card background with clean border & subtle shadow
    draw.rounded_rectangle([x + 3, y + 4, x + w + 3, y + h + 4], radius=14, fill=(241, 245, 249))
    draw.rounded_rectangle([x, y, x + w, y + h], radius=14, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    
    # Header strip inside card
    draw.rounded_rectangle([x, y, x + w, y + 36], radius=14, fill=(248, 250, 252))
    draw.rectangle([x, y + 20, x + w, y + 36], fill=(248, 250, 252)) # square off bottom corners
    draw.line([(x, y + 36), (x + w, y + 36)], fill=(226, 232, 240), width=1)
    
    # Stage pill
    pill_w = 32
    draw.rounded_rectangle([x + 10, y + 7, x + 10 + pill_w, y + 29], radius=6, fill=color)
    draw.text((x + 17, y + 10), stage_num, fill=(255, 255, 255), font=font_tag)
    
    # Title
    draw.text((x + 50, y + 8), title, fill=(15, 23, 42), font=font_card_title)
    
    cy = y + 44
    # Role line
    draw.text((x + 14, cy), "SYSTEM ROLE:", fill=color, font=font_section_h)
    draw.text((x + 100, cy), role, fill=(30, 41, 59), font=font_card_sub)
    cy += 20
    
    # Input Specification
    draw.rounded_rectangle([x + 12, cy, x + w - 12, cy + 34], radius=6, fill=(248, 250, 252), outline=(241, 245, 249), width=1)
    draw.text((x + 18, cy + 3), "INPUT ARTIFACTS:", fill=(100, 116, 139), font=font_tag)
    draw.text((x + 18, cy + 17), in_spec, fill=(15, 23, 42), font=font_code)
    cy += 40
    
    # Core Engine / Components / Invariants (bullets)
    draw.text((x + 14, cy), "ARCHITECTURAL COMPONENTS & PIPELINE:", fill=(15, 23, 42), font=font_section_h)
    cy += 18
    for item in core_tech:
        draw.text((x + 14, cy), "•", fill=color, font=font_card_sub)
        draw.text((x + 25, cy), item, fill=(51, 65, 85), font=font_card_sub)
        cy += 18
        
    cy += 2
    # Output Specification
    draw.rounded_rectangle([x + 12, cy, x + w - 12, cy + 34], radius=6, fill=(240, 253, 250) if color == C01 else (240, 249, 255), outline=(204, 251, 241) if color == C01 else (224, 242, 254), width=1)
    draw.text((x + 18, cy + 3), "OUTPUT CONTRACT:", fill=(13, 148, 136) if color == C01 else (2, 132, 199), font=font_tag)
    draw.text((x + 18, cy + 17), out_spec, fill=(15, 23, 42), font=font_code_b)
    cy += 40
    
    # Key Metric Pill Footer
    draw.rounded_rectangle([x + 12, cy, x + w - 12, cy + 24], radius=6, fill=(241, 245, 249))
    draw.text((x + 18, cy + 5), "BENCHMARK: " + metrics, fill=(71, 85, 105), font=font_tag)

# Card 01: ContextPrism (Bottom-Left)
draw_tech_card(
    x=45, y=775, w=380, h=245,
    stage_num="01",
    title="ContextPrism: Ingestion",
    role="Zero-Trust Ingestion & Context Reduction",
    in_spec="Video (.mp4/.webm), HAR HTTP logs, console.log, AST files",
    core_tech=[
        "Regex PII Sanitizer: strips Bearer tokens, cookies, auth headers",
        "OpenCV 4.10 Adaptive Keyframe Extractor (Laplacian var > 100)",
        "AST Skeletonizer: strips implementation, retains interface signatures",
        "Chronological anchor sync: lockstep network with video timeline"
    ],
    out_spec="Sanitized Keyframes + Sanitized HAR + AST Skeletons",
    metrics="84.9% Token Reduction | 100% PII Masking | Sub-250ms Processing",
    color=C01
)

# Card 02: ApexTrace (Top-Left / Center)
draw_tech_card(
    x=460, y=135, w=390, h=245,
    stage_num="02",
    title="ApexTrace: Dual-Engine",
    role="Multimodal Reasoning & Mathematical Sentinel",
    in_spec="Sanitized Keyframe Sequence + AST Interfaces + Failure Timeline",
    core_tech=[
        "Engine A (Semantic): Gemini 3.1 Flash-Lite JSON API reasoning",
        "Engine B (Deterministic): Pillow SSIM Covariance & Pixel Delta",
        "Zero-Hallucination Crosscheck: validates UI DOM changes vs claims",
        "Anchor Identification: isolates timestamp where state corrupted"
    ],
    out_spec="Hypothesis Vector + Root Cause Anchor + Pixel Delta Proof",
    metrics="Sub-2.4s Inference | SSIM Variance < 0.08 | Zero Visual Hallucination",
    color=C02
)

# Card 03: Consensus Arbiter (Top-Right / Center)
draw_tech_card(
    x=875, y=135, w=395, h=245,
    stage_num="03",
    title="Consensus Arbiter",
    role="Strict 3-Tier Precedence & Bayesian Scoring",
    in_spec="Engine A Hypotheses + Engine B SSIM Covariance Matrix",
    core_tech=[
        "Tier 1 (Deterministic): HTTP 4xx/5xx & unhandled JS errors rule first",
        "Tier 2 (Silent Failure): Click detected + 0.00% pixel repaint flagged",
        "Tier 3 (Visual Noise): CSS jitter & sub-pixel rendering discarded",
        "Bayesian Scoring: C = w_net*S_net + w_err*S_err + w_ssim*S_ssim"
    ],
    out_spec="Certified Defect Decision (94.8% Conf) + Target Patch Spec",
    metrics="100% False-Positive Rejection | Zero Conflicting Diagnoses",
    color=C03
)

# Card 04: Replay Shield (Bottom-Right)
draw_tech_card(
    x=950, y=775, w=410, h=245,
    stage_num="04",
    title="Replay Shield: Sandbox",
    role="Hermetic Test Synthesis & Verification Loop",
    in_spec="Target Patch Spec + Sanitized Network Traces + UI Locators",
    core_tech=[
        "Playwright AST Synthesizer: constructs accessible test locators",
        "Isolated Docker Sandbox (node:20-bookworm-slim + Chromium)",
        "RED Phase: executes test on unmodified code -> confirms repro",
        "GREEN Phase: applies unified diff patch -> validates 100% pass"
    ],
    out_spec="Verified Playwright Spec (.spec.ts) + Clean Patch Diff (.patch)",
    metrics="100% Deterministic Replay | Zero Host Contamination | TDD Loop",
    color=C04
)

# Card 05: VERDE-Hydra Telemetry & PR (Far-Right Upper)
draw_tech_card(
    x=1390, y=135, w=480, h=470,
    stage_num="05",
    title="VERDE-Hydra Telemetry & PR",
    role="Green ESG Energy Audit & GitHub Dispatch",
    in_spec="Verified Patch + Playwright Test + Sandbox CPU Runtime Telemetry",
    core_tech=[
        "Google Cloud Telemetry: PUE = 1.10 (Data Center Efficiency)",
        "Water Consumption Standard: Global WUE = 1.80 L/kWh cooling",
        "Dynamic CPU Power Model: Intel Xeon Platinum (TDP: 205W, Idle: 65W)",
        "Energy Delta Formula: E = (P_active * t_run) + (P_idle * t_wait) Joules",
        "Autonomous Run: ~12s @ 85W = 0.28 Wh | 0.50 ml H2O | 0.12 g CO2e",
        "Manual Engineer Triage: ~45m @ 120W = 90.0 Wh | 162.0 ml H2O",
        "Automated GitHub Draft PR Generator: writes pr_payload.md",
        "CI/CD Integration: Webhook triggers automated branch merge checks"
    ],
    out_spec="Reviewer-Ready GitHub Draft PR + ESG Sustainability Ledger",
    metrics="99.7% Energy & Water Reduction | Audit-Grade Carbon Evidence",
    color=C05
)

# Connector from Stone 05 to Card 05
draw.line([(1305 + BW//2, 410), (1390, 410)], fill=C05, width=2)
draw.polygon([(1390, 410), (1382, 405), (1382, 415)], fill=C05)

# 5. Enterprise Governance & Security Matrix (Bottom Right Card)
mx_x, mx_y, mx_w, mx_h = 1390, 625, 480, 395
draw.rounded_rectangle([mx_x + 3, mx_y + 4, mx_x + mx_w + 3, mx_y + mx_h + 4], radius=14, fill=(241, 245, 249))
draw.rounded_rectangle([mx_x, mx_y, mx_x + mx_w, mx_y + mx_h], radius=14, fill=(255, 255, 255), outline=(226, 232, 240), width=1)

# Header
draw.rounded_rectangle([mx_x, mx_y, mx_x + mx_w, mx_y + 36], radius=14, fill=(248, 250, 252))
draw.rectangle([mx_x, mx_y + 20, mx_x + mx_w, mx_y + 36], fill=(248, 250, 252))
draw.line([(mx_x, mx_y + 36), (mx_x + mx_w, mx_y + 36)], fill=(226, 232, 240), width=1)

# Shield Badge
draw.rounded_rectangle([mx_x + 10, mx_y + 7, mx_x + 42, mx_y + 29], radius=6, fill=(15, 23, 42))
draw.text((mx_x + 16, mx_y + 10), "SEC", fill=(255, 255, 255), font=font_tag)
draw.text((mx_x + 50, mx_y + 8), "Enterprise Governance & Security Matrix", fill=(15, 23, 42), font=font_card_title)

gy = mx_y + 46
gov_items = [
    ("Zero-Trust Ephemeral Sandboxing", "Every Playwright replay runs inside an ephemeral, non-root Docker container with network egress locked after package install. Sandbox is destroyed post-execution."),
    ("Strict SOC2 / GDPR Data Boundary", "No raw user PII, passwords, session cookies, or customer payloads ever leave the ingestion perimeter. Regex scrubs Bearer tokens prior to LLM submission."),
    ("Mathematical Defect Rejection", "Arbiter rejects any visual failure claim unless validated by both SSIM covariance (<0.92) and non-zero console/network failure anchors."),
    ("GitOps Automated Dispatch", "Certified patches are dispatched directly via GitHub REST API as draft pull requests with cryptographic evidence hashes attached.")
]

for g_title, g_desc in gov_items:
    draw.text((mx_x + 14, gy), "■ " + g_title, fill=(15, 23, 42), font=font_section_h)
    gy += 17
    # Wrap description to 2 lines
    words = g_desc.split()
    line1, line2 = "", ""
    for w in words:
        if len(line1) + len(w) < 58:
            line1 += w + " "
        else:
            line2 += w + " "
    draw.text((mx_x + 26, gy), line1.strip(), fill=(71, 85, 105), font=font_card_sub)
    gy += 16
    if line2:
        draw.text((mx_x + 26, gy), line2.strip(), fill=(71, 85, 105), font=font_card_sub)
        gy += 16
    gy += 8

# Overall Pipeline Summary / Architecture Guarantee Strip (Bottom Bar)
bot_y = H - margin - 35
draw.line([(head_x, bot_y - 10), (W - head_x, bot_y - 10)], fill=(241, 245, 249), width=1)

draw.text((head_x, bot_y), "ARCHITECTURAL INVARIANTS:", fill=(15, 23, 42), font=font_section_h)
draw.text((head_x + 195, bot_y + 1), "Hermetic Docker Isolation  ·  Deterministic 3-Tier Precedence  ·  Bimodal Gemini + SSIM Sentinel  ·  Zero Context Poisoning", fill=(100, 116, 139), font=font_code)

status_txt = "Pipeline Status: Fully Operational on Port 8000"
bbox = draw.textbbox((0, 0), status_txt, font=font_code_b)
tw = bbox[2] - bbox[0]
draw.text((W - head_x - tw, bot_y + 1), status_txt, fill=(16, 185, 129), font=font_code_b)

# Save Outputs
buildathon_out = "C:/Users/Dhairya/Desktop/Active/Buildathon/solution_architecture_verdant.png"
desktop_out = "C:/Users/Dhairya/Desktop/solution_architecture_verdant.png"
img.save(buildathon_out, "PNG")
img.save(desktop_out, "PNG")

print(f"Successfully generated high-density solution architecture slide at:\n  - {buildathon_out}\n  - {desktop_out}")
