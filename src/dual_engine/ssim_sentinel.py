"""
Engine B - Mathematical SSIM & Pixel-Delta Sentinel
Custom implementation of Structural Similarity (SSIM) and Bounding-Box Delta Clustering.
Zero external CV framework bloat (uses lightweight standard Python array math).
"""
import math
from typing import Tuple, Dict, Any, List
from PIL import Image

def compute_frame_diff(img1: Image.Image, img2: Image.Image, threshold: float = 0.92) -> Dict[str, Any]:
    """
    Computes mathematical structural similarity and identifies bounding box of change.
    """
    # 1. Downscale to 360p for fast-pass evaluation
    res = (320, 180)
    g1 = img1.resize(res).convert("L")
    g2 = img2.resize(res).convert("L")
    
    b1 = list(g1.getdata())
    b2 = list(g2.getdata())
    n = len(b1)
    
    if n == 0:
        return {"ssim": 1.0, "delta_pct": 0.0, "has_transition": False, "bbox": None}
    
    # 2. Mean & Variance calculation
    mean1 = sum(b1) / n
    mean2 = sum(b2) / n
    
    var1 = sum((x - mean1) ** 2 for x in b1) / n
    var2 = sum((x - mean2) ** 2 for x in b2) / n
    cov = sum((x - mean1) * (y - mean2) for x, y in zip(b1, b2)) / n
    
    c1 = (0.01 * 255) ** 2
    c2 = (0.03 * 255) ** 2
    
    ssim = ((2 * mean1 * mean2 + c1) * (2 * cov + c2)) / ((mean1**2 + mean2**2 + c1) * (var1 + var2 + c2))
    ssim = max(0.0, min(1.0, ssim))
    
    # 3. Absolute Pixel Delta
    diff_pixels = 0
    min_x, min_y, max_x, max_y = res[0], res[1], 0, 0
    
    for idx, (p1, p2) in enumerate(zip(b1, b2)):
        if abs(p1 - p2) > 20: # noise gate
            diff_pixels += 1
            x = idx % res[0]
            y = idx // res[0]
            min_x = min(min_x, x)
            max_x = max(max_x, x)
            min_y = min(min_y, y)
            max_y = max(max_y, y)
            
    delta_pct = (diff_pixels / n) * 100.0
    has_transition = (ssim < threshold) or (delta_pct > 0.8)
    
    # Scale bbox back to original image space
    scale_x = img1.width / res[0]
    scale_y = img1.height / res[1]
    bbox = None
    if diff_pixels > 0 and min_x <= max_x:
        bbox = {
            "x": int(min_x * scale_x),
            "y": int(min_y * scale_y),
            "w": int((max_x - min_x) * scale_x),
            "h": int((max_y - min_y) * scale_y)
        }
        
    return {
        "ssim": round(ssim, 4),
        "delta_pct": round(delta_pct, 2),
        "has_transition": has_transition,
        "bbox": bbox
    }
