"""
Dual-Engine Consensus Arbiter
Executes the 3-Tier Precedence Hierarchy and Multi-Evidence Confidence Scoring.
"""
from typing import Dict, Any, List

def arbitrate_decision(
    gemini_verdict: Dict[str, Any],
    pixel_sentinel: Dict[str, Any],
    network_errors: List[Dict[str, Any]],
    console_errors: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Arbitrates conflicts between Gemini semantic reasoning and deterministic signals.
    """
    has_network_err = len(network_errors) > 0
    has_console_err = len(console_errors) > 0
    has_visual_delta = pixel_sentinel.get("has_transition", False)
    pixel_delta_pct = pixel_sentinel.get("delta_pct", 0.0)
    
    # Tier 1: System / Network / Console Log Absolute Precedence
    if has_network_err or has_console_err:
        err_msg = network_errors[0] if has_network_err else console_errors[0]
        confidence = "HIGH" if (has_network_err and has_console_err) else "MEDIUM"
        return {
            "status": "BUG_CONFIRMED",
            "arbiter_tier": 1,
            "root_cause_type": "API_OR_RUNTIME_EXCEPTION",
            "confidence": confidence,
            "primary_evidence": err_msg,
            "coordinate_override": pixel_sentinel.get("bbox"),
            "summary": "Technical fault confirmed via direct network/console diagnostics."
        }
        
    # Tier 2: Silent UI Freeze (User interacted, but zero visual repaint)
    gemini_claims_action = gemini_verdict.get("user_action_attempted", False)
    if gemini_claims_action and pixel_delta_pct < 0.1:
        return {
            "status": "BUG_CONFIRMED",
            "arbiter_tier": 2,
            "root_cause_type": "SILENT_UI_FREEZE",
            "confidence": "HIGH",
            "primary_evidence": {"delta_pct": pixel_delta_pct, "expected_action": gemini_verdict.get("intent")},
            "coordinate_override": pixel_sentinel.get("bbox"),
            "summary": "Silent freeze detected: User clicked element but zero visual delta occurred."
        }
        
    # Tier 3: Benign Visual Noise vs Real Visual Defect
    if pixel_delta_pct > 15.0 and not gemini_claims_action and not has_network_err:
        return {
            "status": "DISCARDED_AS_NOISE",
            "arbiter_tier": 3,
            "root_cause_type": "BENIGN_ANIMATION",
            "confidence": "LOW",
            "primary_evidence": {"delta_pct": pixel_delta_pct},
            "coordinate_override": None,
            "summary": "High pixel variation without associated user interaction or DOM mutation (ignored)."
        }
        
    # Standard Verified Flow
    return {
        "status": "VERIFIED_DEFECT" if gemini_verdict.get("bug_detected") else "NORMAL",
        "arbiter_tier": 3,
        "root_cause_type": gemini_verdict.get("category", "APPLICATION_LOGIC"),
        "confidence": "MEDIUM",
        "primary_evidence": gemini_verdict,
        "coordinate_override": pixel_sentinel.get("bbox"),
        "summary": gemini_verdict.get("explanation", "Standard analysis completed.")
    }
