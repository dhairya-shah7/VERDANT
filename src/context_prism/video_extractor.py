"""
ContextPrism Real Video Ingestion & Frame Sampling Engine
Uses OpenCV to extract real frames, calculate true duration, and measure pixel deltas.
"""
import os
import cv2
import numpy as np
from PIL import Image
from typing import Dict, Any, List, Tuple
from ..dual_engine.ssim_sentinel import compute_frame_diff

def extract_and_analyze_video(video_path: str, max_samples: int = 12) -> Dict[str, Any]:
    """
    Extracts real frames from an uploaded MP4/WebM video and runs SSIM frame-to-frame diffing.
    """
    if not os.path.exists(video_path):
        return {
            "error": "Video file not found",
            "total_frames": 0,
            "duration_sec": 0.0,
            "ssim": 1.0,
            "delta_pct": 0.0,
            "has_transition": False
        }
        
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        return {
            "error": "Failed to open video codec",
            "total_frames": 0,
            "duration_sec": 0.0,
            "ssim": 1.0,
            "delta_pct": 0.0,
            "has_transition": False
        }
        
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    duration_sec = round(total_frames / max(1.0, fps), 2)
    
    if total_frames <= 0:
        cap.release()
        return {
            "total_frames": 0,
            "duration_sec": 0.0,
            "ssim": 1.0,
            "delta_pct": 0.0,
            "has_transition": False
        }
        
    # Sample up to max_samples evenly spaced frames
    step = max(1, total_frames // max_samples)
    sampled_frames: List[Image.Image] = []
    
    for frame_idx in range(0, total_frames, step):
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
        ret, frame = cap.read()
        if ret and frame is not None:
            # OpenCV is BGR -> convert to RGB PIL Image
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            pil_img = Image.fromarray(rgb_frame)
            sampled_frames.append(pil_img)
            if len(sampled_frames) >= max_samples:
                break
                
    cap.release()
    
    if len(sampled_frames) < 2:
        return {
            "total_frames": total_frames,
            "fps": round(fps, 1),
            "duration_sec": duration_sec,
            "sampled_count": len(sampled_frames),
            "ssim": 1.0,
            "delta_pct": 0.0,
            "has_transition": False
        }
        
    # Run consecutive SSIM diffs across sampled frames
    ssim_scores = []
    delta_scores = []
    for i in range(len(sampled_frames) - 1):
        diff = compute_frame_diff(sampled_frames[i], sampled_frames[i+1])
        ssim_scores.append(diff["ssim"])
        delta_scores.append(diff["delta_pct"])
        
    avg_ssim = sum(ssim_scores) / len(ssim_scores)
    avg_delta = sum(delta_scores) / len(delta_scores)
    min_ssim = min(ssim_scores)
    max_delta = max(delta_scores)
    
    # Freeze detection: If any consecutive window has near-zero delta while user expects mutation
    has_freeze = any(d < 0.05 and s > 0.98 for s, d in zip(ssim_scores, delta_scores))
    has_transition = min_ssim < 0.92 or max_delta > 1.5

    # Save keyframes (start, max transition/freeze frame, end) for Gemini multimodal analysis
    keyframe_paths = []
    try:
        keyframes_dir = os.path.join(os.path.dirname(video_path), "keyframes")
        os.makedirs(keyframes_dir, exist_ok=True)
        video_stem = os.path.splitext(os.path.basename(video_path))[0]

        indices_to_save = [0]
        if delta_scores:
            max_delta_idx = delta_scores.index(max(delta_scores))
            indices_to_save.append(min(max_delta_idx + 1, len(sampled_frames) - 1))
        indices_to_save.append(len(sampled_frames) - 1)
        indices_to_save = sorted(list(set(indices_to_save)))

        for idx in indices_to_save:
            kf_path = os.path.join(keyframes_dir, f"{video_stem}_kf_{idx}.png")
            sampled_frames[idx].save(kf_path, "PNG")
            keyframe_paths.append(kf_path)
    except Exception as e:
        print(f"[VideoExtractor] Keyframe save warning: {e}")
    
    return {
        "total_frames": total_frames,
        "fps": round(fps, 1),
        "duration_sec": duration_sec,
        "sampled_count": len(sampled_frames),
        "ssim": round(avg_ssim, 4),
        "min_ssim": round(min_ssim, 4),
        "delta_pct": round(avg_delta, 2),
        "max_delta_pct": round(max_delta, 2),
        "has_transition": has_transition,
        "has_freeze": has_freeze,
        "keyframe_paths": keyframe_paths
    }
