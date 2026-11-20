"""
Visual Infographic Generator for Slide 7: Google AI Models Architecture
Builds a visual-first, high-impact enterprise diagram:
- Visual Input Stream: Filmstrip, AST Code bracket, HAR network pulse
- Central AI Neural Microprocessor: Google Gemini Core with pinouts and routing tracks
- Live Infographic Meters: 94.8% Circular Gauge, 2.4s Latency Bar, 0.28 Wh Green Meter
- Visual Output Artifacts: Playwright Test Terminal, Git Unified Patch, PR Card
- Stage-by-Stage Mapping Labels connecting every visual node to V.E.R.D.A.N.T. stages
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
font_node_title = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 17)
font_node_sub = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 12)
font_metric_num = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 26)
font_metric_lbl = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 11)
font_code = ImageFont.truetype("C:/Windows/Fonts/consola.ttf", 11)
font_code_b = ImageFont.truetype("C:/Windows/Fonts/consolab.ttf", 11)
font_tag = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 11)
font_badge = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 12)

# 1. Main Slide Border & Shadow
margin = 25
draw.rounded_rectangle([margin, margin, W - margin, H - margin], radius=22, fill=(255, 255, 255), outline=(226, 232, 240), width=2)

# 2. Header
head_x, head_y = 65, 50
g_colors = [(66, 133, 244), (234, 67, 53), (251, 188, 5), (52, 168, 83)]
for i, gc in enumerate(g_colors):
    draw.rounded_rectangle([head_x + i * 12, head_y, head_x + i * 12 + 8, head_y + 36], radius=4, fill=gc)

draw.text((head_x + 60, head_y - 6), "Google AI Models Architecture & Visual Pipeline", fill=(15, 23, 42), font=font_title)
draw.text((head_x + 62, head_y + 40), "Visual-to-Code Neural Routing Engine: Ingestion ➔ Gemini 3.1 Flash-Lite ➔ Consensus ➔ Synthesizer", fill=(100, 116, 139), font=font_sub)

# Top Right Badges
rb_y = head_y + 2
b1_w = 265
b1_x = W - margin - b1_w - 50
draw.rounded_rectangle([b1_x, rb_y, b1_x + b1_w, rb_y + 36], radius=18, fill=(240, 253, 244), outline=(187, 247, 208), width=1)
draw.text((b1_x + 18, rb_y + 9), "Google Cloud & DeepMind 2026", fill=(21, 128, 61), font=font_badge)

b2_w = 195
b2_x = b1_x - b2_w - 14
draw.rounded_rectangle([b2_x, rb_y, b2_x + b2_w, rb_y + 36], radius=18, fill=(239, 246, 255), outline=(191, 219, 254), width=1)
draw.text((b2_x + 16, rb_y + 9), "● Model Routing Matrix", fill=(29, 78, 216), font=font_badge)

draw.line([(head_x, head_y + 78), (W - head_x, head_y + 78)], fill=(241, 245, 249), width=1)

# -------------------------------------------------------------
# COLUMN 1: VISUAL INPUT TIER (x: 65 to 480)
# -------------------------------------------------------------
in_x = head_x
in_y = 155
in_w = 385
in_h = 820

draw.rounded_rectangle([in_x + 3, in_y + 4, in_x + in_w + 3, in_y + in_h + 4], radius=18, fill=(235, 240, 246))
draw.rounded_rectangle([in_x, in_y, in_x + in_w, in_y + in_h], radius=18, fill=(255, 255, 255), outline=(226, 232, 240), width=1)

# Header
draw.rounded_rectangle([in_x, in_y, in_x + in_w, in_y + 45], radius=18, fill=(248, 250, 252))
draw.rectangle([in_x, in_y + 25, in_x + in_w, in_y + 45], fill=(248, 250, 252))
draw.line([(in_x, in_y + 45), (in_x + in_w, in_y + 45)], fill=(226, 232, 240), width=1)
draw.text((in_x + 18, in_y + 12), "INPUT MULTIMODAL TELEMETRY", fill=(15, 23, 42), font=font_node_title)

# Artifact 1: Filmstrip Graphic (Video Ingestion)
fs_y = in_y + 65
draw.text((in_x + 18, fs_y), "01 · VIDEO REPLAY KEYFRAMES (MP4)", fill=(147, 51, 234), font=font_tag)
# Draw Filmstrip
fs_w, fs_h = 345, 110
fs_box_y = fs_y + 22
draw.rounded_rectangle([in_x + 18, fs_box_y, in_x + 18 + fs_w, fs_box_y + fs_h], radius=8, fill=(30, 41, 59))
# Film perforations top & bottom
for p in range(in_x + 24, in_x + 18 + fs_w - 12, 24):
    draw.rounded_rectangle([p, fs_box_y + 5, p + 12, fs_box_y + 14], radius=2, fill=(255, 255, 255))
    draw.rounded_rectangle([p, fs_box_y + fs_h - 14, p + 12, fs_box_y + fs_h - 5], radius=2, fill=(255, 255, 255))

# 3 Video Frames inside filmstrip
frame_w = 92
frame_h = 66
frame_y = fs_box_y + 22
frames_x = [in_x + 28, in_x + 142, in_x + 256]
colors_f = [(15, 118, 110), (14, 116, 144), (220, 38, 38)]
labels_f = ["00:06 (Click)", "00:12 (Freeze)", "00:18 (Error 500)"]
for i, fx in enumerate(frames_x):
    draw.rectangle([fx, frame_y, fx + frame_w, frame_y + frame_h], fill=(15, 23, 42), outline=colors_f[i], width=2)
    # UI wireframe inside frame
    draw.rectangle([fx + 8, frame_y + 10, fx + 50, frame_y + 16], fill=(71, 85, 105))
    draw.rectangle([fx + 8, frame_y + 24, fx + 80, frame_y + 44], fill=(51, 65, 85))
    draw.rounded_rectangle([fx + 25, frame_y + 50, fx + 65, frame_y + 60], radius=3, fill=colors_f[i])
    draw.text((fx + 4, frame_y + 48), labels_f[i], fill=(255, 255, 255), font=font_code)

# Artifact 2: AST Code Interface Skeleton Box
ast_y = fs_box_y + fs_h + 35
draw.text((in_x + 18, ast_y), "02 · AST CODE INTERFACE (SKELETON)", fill=(66, 133, 244), font=font_tag)
ast_box_y = ast_y + 22
draw.rounded_rectangle([in_x + 18, ast_box_y, in_x + 18 + fs_w, ast_box_y + 155], radius=8, fill=(15, 23, 42), outline=(51, 65, 85), width=1)
# Terminal buttons
draw.ellipse([in_x + 30, ast_box_y + 10, in_x + 38, ast_box_y + 18], fill=(239, 68, 68))
draw.ellipse([in_x + 44, ast_box_y + 10, in_x + 52, ast_box_y + 18], fill=(245, 158, 11))
draw.ellipse([in_x + 58, ast_box_y + 10, in_x + 66, ast_box_y + 18], fill=(16, 185, 129))
draw.text((in_x + 80, ast_box_y + 8), "cart_service.ts (AST Skel)", fill=(148, 163, 184), font=font_code)

# Code lines
clines = [
    ("interface CartState {", (226, 232, 240)),
    ("  cartId?: string; // Pruned: -84.9% tokens", (100, 116, 139)),
    ("  items: CartItem[];", (226, 232, 240)),
    ("}", (226, 232, 240)),
    ("export function checkout(s: CartState): Promise {", (56, 189, 248)),
    ("  // [Implementation distilled by AST engine]", (100, 116, 139)),
    ("}", (56, 189, 248))
]
cy = ast_box_y + 32
for cl, col in clines:
    draw.text((in_x + 28, cy), cl, fill=col, font=font_code)
    cy += 16

# Artifact 3: HAR Network Stream Wave Box
har_y = ast_box_y + 175
draw.text((in_x + 18, har_y), "03 · NETWORK HAR & CONSOLE TRACES", fill=(217, 119, 6), font=font_tag)
har_box_y = har_y + 22
draw.rounded_rectangle([in_x + 18, har_box_y, in_x + 18 + fs_w, har_box_y + 125], radius=8, fill=(248, 250, 252), outline=(226, 232, 240), width=1)
# Draw HTTP Request log pills
logs = [
    ("POST /api/v1/checkout", "HTTP 500 Internal", (220, 38, 38), (254, 242, 242)),
    ("TypeError: undefined cartId", "Console Exception", (234, 88, 12), (255, 247, 237)),
    ("GET /api/v1/health", "HTTP 200 OK", (16, 185, 129), (240, 253, 244))
]
ly = har_box_y + 12
for endpoint, status, text_col, bg_col in logs:
    draw.rounded_rectangle([in_x + 28, ly, in_x + 18 + fs_w - 12, ly + 28], radius=6, fill=bg_col, outline=text_col, width=1)
    draw.text((in_x + 36, ly + 6), endpoint, fill=(15, 23, 42), font=font_code_b)
    draw.text((in_x + 230, ly + 6), status, fill=text_col, font=font_code_b)
    ly += 36

# Bottom Annotation on Input Tier
draw.rounded_rectangle([in_x + 18, in_y + in_h - 95, in_x + in_w - 18, in_y + in_h - 20], radius=8, fill=(240, 253, 244), outline=(187, 247, 208), width=1)
draw.text((in_x + 28, in_y + in_h - 85), "WHERE IT IS USED: STAGE 01", fill=(21, 128, 61), font=font_node_title)
draw.text((in_x + 28, in_y + in_h - 62), "ContextPrism extracts OpenCV keyframes & AST interfaces,", fill=(71, 85, 105), font=font_node_sub)
draw.text((in_x + 28, in_y + in_h - 45), "feeding pristine bimodal tokens to Google AI Models.", fill=(71, 85, 105), font=font_node_sub)

# -------------------------------------------------------------
# COLUMN 2: CENTRAL GOOGLE AI PROCESSOR & ROUTING ENGINE (x: 485 to 1345)
# -------------------------------------------------------------
core_x = 485
core_y = in_y
core_w = 860
core_h = in_h

draw.rounded_rectangle([core_x + 3, core_y + 4, core_x + core_w + 3, core_y + core_h + 4], radius=18, fill=(235, 240, 246))
draw.rounded_rectangle([core_x, core_y, core_x + core_w, core_y + core_h], radius=18, fill=(255, 255, 255), outline=(226, 232, 240), width=1)

# Core Header
draw.rounded_rectangle([core_x, core_y, core_x + core_w, core_y + 45], radius=18, fill=(248, 250, 252))
draw.rectangle([core_x, core_y + 25, core_x + core_w, core_y + 45], fill=(248, 250, 252))
draw.line([(core_x, core_y + 45), (core_x + core_w, core_y + 45)], fill=(226, 232, 240), width=1)
draw.text((core_x + 24, core_y + 12), "GOOGLE AI MODELS CORE ENGINE & MULTIMODAL ROUTING", fill=(15, 23, 42), font=font_node_title)

# The Central Microprocessor Graphic (Visual IC Chip)
chip_cx = core_x + core_w // 2
chip_cy = core_y + 185
chip_w, chip_h = 320, 175

# Chip Pins (Left & Right connectors)
for py in range(chip_cy - chip_h//2 + 20, chip_cy + chip_h//2 - 10, 24):
    draw.rectangle([chip_cx - chip_w//2 - 14, py, chip_cx - chip_w//2, py + 10], fill=(203, 213, 225))
    draw.rectangle([chip_cx + chip_w//2, py, chip_cx + chip_w//2 + 14, py + 10], fill=(203, 213, 225))

# Chip Body
draw.rounded_rectangle([chip_cx - chip_w//2, chip_cy - chip_h//2, chip_cx + chip_w//2, chip_cy + chip_h//2], radius=14, fill=(15, 23, 42), outline=(51, 65, 85), width=2)
# Chip Center Core (Glowing Silicon Die)
die_w, die_h = 240, 115
draw.rounded_rectangle([chip_cx - die_w//2, chip_cy - die_h//2, chip_cx + die_w//2, chip_cy + die_h//2], radius=8, fill=(30, 41, 59), outline=(66, 133, 244), width=2)

# Stylized Google Gemini 4-Point Star in Center
star_x, star_y = chip_cx, chip_cy - 12
draw.polygon([(star_x, star_y - 28), (star_x + 8, star_y - 8), (star_x + 28, star_y), (star_x + 8, star_y + 8), (star_x, star_y + 28), (star_x - 8, star_y + 8), (star_x - 28, star_y), (star_x - 8, star_y - 8)], fill=(66, 133, 244))
draw.polygon([(star_x, star_y - 18), (star_x + 5, star_y - 5), (star_x + 18, star_y), (star_x + 5, star_y + 5), (star_x, star_y + 18), (star_x - 5, star_y + 5), (star_x - 18, star_y), (star_x - 5, star_y - 5)], fill=(255, 255, 255))

draw.text((chip_cx - 95, chip_cy + 22), "GOOGLE GEMINI 3.1", fill=(255, 255, 255), font=font_node_title)
draw.text((chip_cx - 105, chip_cy + 42), "DUAL-ENGINE REASONING KERNEL", fill=(56, 189, 248), font=font_tag)

# Input lines connecting Left Tier to Chip
draw.line([(in_x + in_w, fs_box_y + fs_h//2), (chip_cx - chip_w//2 - 14, chip_cy - 40)], fill=(147, 51, 234), width=2)
draw.line([(in_x + in_w, ast_box_y + 70), (chip_cx - chip_w//2 - 14, chip_cy)], fill=(66, 133, 244), width=2)
draw.line([(in_x + in_w, har_box_y + 60), (chip_cx - chip_w//2 - 14, chip_cy + 40)], fill=(217, 119, 6), width=2)

# 2 Parallel Processing Pods below Chip:
# Pod A: Gemini 3.1 Flash-Lite (Semantic Code Analysis)
# Pod B: Gemini Multimodal Vision (DOM & Keyframe Correlation)

pod_w = 385
pod_h = 205
pod_y = chip_cy + chip_h//2 + 35

# POD A (Left)
podA_x = core_x + 35
draw.rounded_rectangle([podA_x, pod_y, podA_x + pod_w, pod_y + pod_h], radius=12, fill=(248, 250, 252), outline=(66, 133, 244), width=1)
# Top Bar
draw.rounded_rectangle([podA_x, pod_y, podA_x + pod_w, pod_y + 36], radius=12, fill=(239, 246, 255))
draw.rectangle([podA_x, pod_y + 20, podA_x + pod_w, pod_y + 36], fill=(239, 246, 255))
draw.line([(podA_x, pod_y + 36), (podA_x + pod_w, pod_y + 36)], fill=(219, 234, 254), width=1)
draw.text((podA_x + 16, pod_y + 8), "GEMINI 3.1 FLASH-LITE", fill=(29, 78, 216), font=font_node_title)
draw.text((podA_x + pod_w - 95, pod_y + 10), "SEMANTIC CORE", fill=(37, 99, 235), font=font_tag)

# Where used chip
draw.rounded_rectangle([podA_x + 14, pod_y + 44, podA_x + pod_w - 14, pod_y + 72], radius=6, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
draw.text((podA_x + 22, pod_y + 50), "WHERE USED: STAGE 02 (APEXTRACE ENGINE A)", fill=(15, 23, 42), font=font_code_b)

draw.text((podA_x + 16, pod_y + 82), "• Ingests AST skeletons & stack traces in sub-2.4s", fill=(71, 85, 105), font=font_node_sub)
draw.text((podA_x + 16, pod_y + 102), "• Isolates failure anchor state.cart?.cartId", fill=(71, 85, 105), font=font_node_sub)
draw.text((podA_x + 16, pod_y + 122), "• Ultra-low energy profile: 0.28 Wh per execution", fill=(71, 85, 105), font=font_node_sub)
draw.text((podA_x + 16, pod_y + 142), "• Zero model drift across repeated test cycles", fill=(71, 85, 105), font=font_node_sub)

draw.rounded_rectangle([podA_x + 14, pod_y + 168, podA_x + pod_w - 14, pod_y + 194], radius=6, fill=(239, 246, 255))
draw.text((podA_x + 22, pod_y + 174), "Model: gemini-3.1-flash-lite · Temp: 0.2 · Low TTFT", fill=(29, 78, 216), font=font_code)

# POD B (Right)
podB_x = core_x + core_w - 35 - pod_w
draw.rounded_rectangle([podB_x, pod_y, podB_x + pod_w, pod_y + pod_h], radius=12, fill=(248, 250, 252), outline=(147, 51, 234), width=1)
# Top Bar
draw.rounded_rectangle([podB_x, pod_y, podB_x + pod_w, pod_y + 36], radius=12, fill=(250, 245, 255))
draw.rectangle([podB_x, pod_y + 20, podB_x + pod_w, pod_y + 36], fill=(250, 245, 255))
draw.line([(podB_x, pod_y + 36), (podB_x + pod_w, pod_y + 36)], fill=(243, 232, 255), width=1)
draw.text((podB_x + 16, pod_y + 8), "GEMINI MULTIMODAL VISION", fill=(126, 34, 206), font=font_node_title)
draw.text((podB_x + pod_w - 95, pod_y + 10), "VISUAL SENTINEL", fill=(147, 51, 234), font=font_tag)

# Where used chip
draw.rounded_rectangle([podB_x + 14, pod_y + 44, podB_x + pod_w - 14, pod_y + 72], radius=6, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
draw.text((podB_x + 22, pod_y + 50), "WHERE USED: STAGE 01 & 02 (INGEST & APEX)", fill=(15, 23, 42), font=font_code_b)

draw.text((podB_x + 16, pod_y + 82), "• Maps video keyframe clicks to DOM elements", fill=(71, 85, 105), font=font_node_sub)
draw.text((podB_x + 16, pod_y + 102), "• Detects silent UI freeze (click + 0% DOM repaint)", fill=(71, 85, 105), font=font_node_sub)
draw.text((podB_x + 16, pod_y + 122), "• Validates against SSIM mathematical sentinel", fill=(71, 85, 105), font=font_node_sub)
draw.text((podB_x + 16, pod_y + 142), "• Pruned frames prevent video context bloat", fill=(71, 85, 105), font=font_node_sub)

draw.rounded_rectangle([podB_x + 14, pod_y + 168, podB_x + pod_w - 14, pod_y + 194], radius=6, fill=(250, 245, 255))
draw.text((podB_x + 22, pod_y + 174), "Model: gemini-3.1-pro-vision · Bimodal Frame Sync", fill=(126, 34, 206), font=font_code)

# Connector lines from Chip to Pod A and Pod B
draw.line([(chip_cx - 60, chip_cy + chip_h//2), (podA_x + pod_w//2, pod_y)], fill=(66, 133, 244), width=2)
draw.line([(chip_cx + 60, chip_cy + chip_h//2), (podB_x + pod_w//2, pod_y)], fill=(147, 51, 234), width=2)

# Real Visual Infographic Meters (Bottom of Core Column):
# 1. Circular Confidence Gauge (94.8%)
# 2. Latency Speedometer Bar (2.4s)
# 3. Green Energy Meter (0.28 Wh)
meter_y = pod_y + pod_h + 30
meter_h = 175
draw.rounded_rectangle([core_x + 35, meter_y, core_x + core_w - 35, meter_y + meter_h], radius=12, fill=(248, 250, 252), outline=(226, 232, 240), width=1)

# Meter 1: Circular Gauge (Confidence 94.8%)
g1_cx, g1_cy = core_x + 155, meter_y + 75
r_outer = 45
# Background circle
draw.ellipse([g1_cx - r_outer, g1_cy - r_outer, g1_cx + r_outer, g1_cy + r_outer], outline=(226, 232, 240), width=8)
# Progress arc (94.8% ~ 340 degrees)
draw.arc([g1_cx - r_outer, g1_cy - r_outer, g1_cx + r_outer, g1_cy + r_outer], start=-90, end=250, fill=(16, 185, 129), width=8)
draw.text((g1_cx - 26, g1_cy - 14), "94.8%", fill=(15, 23, 42), font=font_node_title)
draw.text((g1_cx - 45, meter_y + 130), "BAYESIAN CONFIDENCE", fill=(100, 116, 139), font=font_metric_lbl)
draw.text((g1_cx - 38, meter_y + 146), "Stage 03 Arbiter", fill=(16, 185, 129), font=font_code_b)

# Divider
draw.line([(core_x + 295, meter_y + 20), (core_x + 295, meter_y + meter_h - 20)], fill=(226, 232, 240), width=1)

# Meter 2: Latency Speed Bar (2.4s TTFT)
m2_x = core_x + 330
draw.text((m2_x, meter_y + 25), "INFERENCE LATENCY (TTFT)", fill=(100, 116, 139), font=font_metric_lbl)
draw.text((m2_x, meter_y + 42), "2.40s", fill=(15, 23, 42), font=font_metric_num)
draw.text((m2_x + 85, meter_y + 54), "vs 45min manual", fill=(100, 116, 139), font=font_code)
# Visual Bar
draw.rounded_rectangle([m2_x, meter_y + 82, m2_x + 210, meter_y + 98], radius=8, fill=(226, 232, 240))
draw.rounded_rectangle([m2_x, meter_y + 82, m2_x + 185, meter_y + 98], radius=8, fill=(66, 133, 244))
draw.text((m2_x, meter_y + 112), "WHERE USED: STAGE 02 APEXTRACE", fill=(29, 78, 216), font=font_code_b)
draw.text((m2_x, meter_y + 130), "High-throughput autonomous bug triage", fill=(71, 85, 105), font=font_node_sub)

# Divider
draw.line([(core_x + 580, meter_y + 20), (core_x + 580, meter_y + meter_h - 20)], fill=(226, 232, 240), width=1)

# Meter 3: Green Energy Leaf & Battery (0.28 Wh)
m3_x = core_x + 615
draw.text((m3_x, meter_y + 25), "GREEN ENERGY FOOTPRINT", fill=(100, 116, 139), font=font_metric_lbl)
draw.text((m3_x, meter_y + 42), "0.28 Wh", fill=(15, 23, 42), font=font_metric_num)
draw.text((m3_x + 120, meter_y + 54), "-99.7% energy", fill=(16, 185, 129), font=font_code_b)
# Visual Battery
draw.rounded_rectangle([m3_x, meter_y + 82, m3_x + 180, meter_y + 98], radius=8, fill=(226, 232, 240))
draw.rounded_rectangle([m3_x, meter_y + 82, m3_x + 25, meter_y + 98], radius=8, fill=(16, 185, 129)) # only 0.28Wh used!
draw.text((m3_x, meter_y + 112), "WHERE USED: STAGE 05 VERDE-HYDRA", fill=(21, 128, 61), font=font_code_b)
draw.text((m3_x, meter_y + 130), "Audited with Google Cloud PUE 1.10", fill=(71, 85, 105), font=font_node_sub)

# -------------------------------------------------------------
# COLUMN 3: VISUAL OUTPUT DELIVERABLES (x: 1365 to 1855)
# -------------------------------------------------------------
out_x = 1365
out_y = in_y
out_w = W - margin - out_x - 30
out_h = in_h

draw.rounded_rectangle([out_x + 3, out_y + 4, out_x + out_w + 3, out_y + out_h + 4], radius=18, fill=(235, 240, 246))
draw.rounded_rectangle([out_x, out_y, out_x + out_w, out_y + out_h], radius=18, fill=(255, 255, 255), outline=(226, 232, 240), width=1)

# Header
draw.rounded_rectangle([out_x, out_y, out_x + out_w, out_y + 45], radius=18, fill=(248, 250, 252))
draw.rectangle([out_x, out_y + 25, out_x + out_w, out_y + 45], fill=(248, 250, 252))
draw.line([(out_x, out_y + 45), (out_x + out_w, out_y + 45)], fill=(226, 232, 240), width=1)
draw.text((out_x + 18, out_y + 12), "OUTPUT VERIFIED DELIVERABLES", fill=(15, 23, 42), font=font_node_title)

# Output Box 1: Playwright Reproducer Spec
pw_y = out_y + 65
draw.text((out_x + 18, pw_y), "WHERE USED: STAGE 04 (REPLAY SHIELD)", fill=(29, 78, 216), font=font_tag)
pw_box_y = pw_y + 22
draw.rounded_rectangle([out_x + 18, pw_box_y, out_x + out_w - 18, pw_box_y + 180], radius=8, fill=(15, 23, 42), outline=(51, 65, 85), width=1)
# Terminal controls
draw.ellipse([out_x + 30, pw_box_y + 10, out_x + 38, pw_box_y + 18], fill=(239, 68, 68))
draw.ellipse([out_x + 44, pw_box_y + 10, out_x + 52, pw_box_y + 18], fill=(245, 158, 11))
draw.ellipse([out_x + 58, pw_box_y + 10, out_x + 66, pw_box_y + 18], fill=(16, 185, 129))
draw.text((out_x + 80, pw_box_y + 8), "reproduce_bug.spec.ts (Verified RED->GREEN)", fill=(148, 163, 184), font=font_code)

pw_lines = [
    ("test('Cart checkout error reproduction', async ({ page }) => {", (56, 189, 248)),
    ("  await page.goto('http://localhost:8000/demo-app');", (226, 232, 240)),
    ("  await page.getByRole('button', { name: 'Checkout' }).click();", (226, 232, 240)),
    ("  // Proves defect reproduction in Docker Sandbox:", (100, 116, 139)),
    ("  await expect(page.locator('.order-success')).toBeVisible();", (244, 63, 94)),
    ("});", (56, 189, 248)),
    ("✔ TEST PASSES ON PATCHED SCRIPT IN DOCKER", (16, 185, 129))
]
pwy = pw_box_y + 32
for pl, col in pw_lines:
    draw.text((out_x + 28, pwy), pl, fill=col, font=font_code)
    pwy += 18

# Output Box 2: Unified Git Patch Diff Box
diff_y = pw_box_y + 198
draw.text((out_x + 18, diff_y), "WHERE USED: STAGE 03 & 04 (ARBITER & REPLAY)", fill=(13, 148, 136), font=font_tag)
diff_box_y = diff_y + 22
draw.rounded_rectangle([out_x + 18, diff_box_y, out_x + out_w - 18, diff_box_y + 160], radius=8, fill=(15, 23, 42), outline=(51, 65, 85), width=1)
draw.text((out_x + 28, diff_box_y + 10), "patch_unified.diff", fill=(148, 163, 184), font=font_code)

d_lines = [
    ("--- a/src/services/cart.ts", (148, 163, 184)),
    ("+++ b/src/services/cart.ts", (148, 163, 184)),
    ("@@ -18,4 +18,4 @@ function submitOrder(state) {", (100, 116, 139)),
    ("-  const id = state.cart.cartId; // Crash: undefined", (244, 63, 94)),
    ("+  const id = state.cart?.cartId ?? generateUUID();", (16, 185, 129)),
    ("   return api.post('/order', { id });", (226, 232, 240)),
    ("}", (226, 232, 240))
]
dy = diff_box_y + 30
for dl, col in d_lines:
    draw.text((out_x + 28, dy), dl, fill=col, font=font_code)
    dy += 18

# Output Box 3: Automated GitHub PR Card
pr_y = diff_box_y + 178
draw.text((out_x + 18, pr_y), "WHERE USED: STAGE 05 (VERDE-HYDRA DISPATCH)", fill=(217, 119, 6), font=font_tag)
pr_box_y = pr_y + 22
draw.rounded_rectangle([out_x + 18, pr_box_y, out_x + out_w - 18, pr_box_y + 185], radius=8, fill=(248, 250, 252), outline=(226, 232, 240), width=1)

# PR Header inside
draw.rounded_rectangle([out_x + 28, pr_box_y + 12, out_x + 95, pr_box_y + 36], radius=6, fill=(240, 253, 244), outline=(187, 247, 208), width=1)
draw.text((out_x + 36, pr_box_y + 16), "✔ OPEN", fill=(21, 128, 61), font=font_code_b)
draw.text((out_x + 110, pr_box_y + 16), "PR #142 · Fix Cart State Mutation", fill=(15, 23, 42), font=font_node_title)

draw.text((out_x + 28, pr_box_y + 48), "• Synthesized by Gemini 3.1 Structured Decoders", fill=(71, 85, 105), font=font_node_sub)
draw.text((out_x + 28, pr_box_y + 68), "• Attached Replay: reproduce_bug.spec.ts (PASS)", fill=(16, 185, 129), font=font_node_sub)
draw.text((out_x + 28, pr_box_y + 88), "• Cryptographic evidence ledger & PII scrub hash", fill=(71, 85, 105), font=font_node_sub)
draw.text((out_x + 28, pr_box_y + 108), "• ESG Telemetry: 99.7% energy reduction validated", fill=(21, 128, 61), font=font_node_sub)

draw.rounded_rectangle([out_x + 28, pr_box_y + 138, out_x + out_w - 28, pr_box_y + 168], radius=6, fill=(15, 23, 42))
draw.text((out_x + 50, pr_box_y + 146), "Auto-Merged via GitHub Actions Webhook", fill=(255, 255, 255), font=font_code_b)

# Connecting Lines from Central Core to Outputs
draw.line([(core_x + core_w, pod_y + 50), (out_x, pw_box_y + 80)], fill=(66, 133, 244), width=2)
draw.line([(core_x + core_w, pod_y + 150), (out_x, diff_box_y + 70)], fill=(13, 148, 136), width=2)
draw.line([(core_x + core_w, meter_y + 100), (out_x, pr_box_y + 80)], fill=(217, 119, 6), width=2)

# Footer
foot_y = H - margin - 35
draw.line([(head_x, foot_y - 10), (W - head_x, foot_y - 10)], fill=(241, 245, 249), width=1)
draw.text((head_x, foot_y), "V.E.R.D.A.N.T. Visual Model Architecture · Startup Buildathon India 2026", fill=(100, 116, 139), font=font_sub)

status_txt = "Pipeline Status: Fully Operational & Verified Live on Port 8000"
bbox = draw.textbbox((0, 0), status_txt, font=font_code_b)
tw = bbox[2] - bbox[0]
draw.text((W - head_x - tw, foot_y), status_txt, fill=(16, 185, 129), font=font_code_b)

# Save high-res PNG outputs
out_buildathon = os.path.normpath(r"C:\Users\Dhairya\Desktop\Active\Buildathon\google_ai_models_verdant.png")
out_desktop = os.path.normpath(r"C:\Users\Dhairya\Desktop\google_ai_models_verdant.png")
img.save(out_buildathon, format="PNG")
img.save(out_desktop, format="PNG")

print(f"Successfully generated Visual Infographic for Google AI Models at:\n  - {out_buildathon}\n  - {out_desktop}")
