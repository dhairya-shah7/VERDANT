"""
V.E.R.D.A.N.T. System Configuration
"""
import os
from pathlib import Path
from dataclasses import dataclass

# Robust .env loader
env_path = Path(__file__).resolve().parent.parent / ".env"
if env_path.exists():
    with open(env_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ[k.strip()] = v.strip()

@dataclass
class Config:
    # Model Selection
    GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite") # Ultra-fast, highly available multimodal tier
    GEMINI_FAST_MODEL: str = os.getenv("GEMINI_FAST_MODEL", "gemini-3.5-flash-lite") # Verified active fast structured tier
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    
    # ContextPrism Thresholds
    SAFETY_ANCHOR_SECONDS: float = 1.5   # Preserve frames ±1.5s around critical events
    SSIM_CHANGE_THRESHOLD: float = 0.92  # Frames with SSIM < 0.92 are treated as scene transitions
    DOWNSCALE_RES: tuple = (640, 360)    # Fast-scan 360p resolution for high throughput
    
    # Arbiter Weights
    WEIGHT_NETWORK: float = 0.35
    WEIGHT_CONSOLE: float = 0.25
    WEIGHT_VISUAL: float = 0.25
    WEIGHT_DOM: float = 0.15
    
    # Green Telemetry Constants (Google Cloud Published Standards)
    PUE_CLOUD: float = 1.10              # Google Cloud Data Center Power Usage Effectiveness
    WUE_COOLING_L_KWH: float = 1.80      # Liters of evaporated water per kWh (cooling)
    ESTIMATED_WH_PER_1K_TOKENS: float = 0.0004
    
    # Sandbox
    SANDBOX_TIMEOUT_SECONDS: int = 30
    DEFAULT_BRANCH_PREFIX: str = "verdant/fix-"

CONFIG = Config()
