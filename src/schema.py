"""
V.E.R.D.A.N.T. v2 Core Typed Schemas
Defines the strict 5-path operational contracts across multimodal reasoning,
atomic patch generation, test synthesis, and eco-telemetry.
Zero mock data: all fields validate real model-generated inference.
"""
from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class ActionType(str, Enum):
    ADVISE = "advise"    # Path A: Architectural explanation or factual query
    FIX = "fix"          # Path B: Surgical code patch with atomic search/replace
    TEST = "test"        # Path C: E2E Playwright test synthesis (no app code changes)
    ENV = "env"          # Path D: Environment / Build / Dependency conflict (1-click terminal command)
    CLARIFY = "clarify"  # Path E: Grounding question when context is ambiguous


class Edit(BaseModel):
    """
    Atomic Search/Replace Pair.
    Guarantees deterministic patching: `search` must match exactly once in `path`.
    """
    path: str = Field(..., description="Repo-relative path of the target source file")
    search: str = Field(..., description="Exact string block in target file to be replaced")
    replace: str = Field(..., description="Drop-in replacement string block")


class TestSpec(BaseModel):
    """
    Playwright or Pytest reproducible test specification.
    """
    path: str = Field(..., description="Repo-relative path for test file, e.g. tests/e2e/test_reproducer.py")
    content: str = Field(..., description="Full source code of the test script")
    runner: str = Field(default="playwright", description="Test runner engine: 'playwright' or 'pytest'")
    target_url: Optional[str] = Field(default=None, description="Target local or staging URL under test")


class EnvAction(BaseModel):
    """
    1-Click Terminal remediation for environmental and dependency failures.
    """
    command: str = Field(..., description="Exact terminal command, e.g. 'kill -9 $(lsof -t -i:3000)'")
    description: str = Field(..., description="Human explanation of what this terminal command achieves")
    action_type: str = Field(default="port_conflict", description="Category: port_conflict, missing_dep, migration, etc.")


class Evidence(BaseModel):
    """
    Grounding evidence extracted across visual, console, and AST layers.
    """
    suspect_file: Optional[str] = Field(default=None, description="Primary source file implicated in the defect")
    line_numbers: List[int] = Field(default_factory=list, description="Specific line numbers implicated")
    error_pattern: Optional[str] = Field(default=None, description="Regex or pattern identifying the failure signature")
    console_log: Optional[str] = Field(default=None, description="Relevant console exception or network failure snippet")


class EcoAudit(BaseModel):
    """
    Formula-backed thermodynamic telemetry based on Google Cloud PUE 1.10 / WUE 1.58 L/kWh.
    """
    energy_wh: float = Field(..., description="Total electrical energy consumed in Watt-hours")
    water_ml: float = Field(..., description="Total cooling water consumed in milliliters")
    tokens_used: int = Field(..., description="Active token count evaluated")
    tokens_saved: int = Field(default=0, description="Tokens eliminated via AST pruning")
    compression_ratio_pct: float = Field(default=0.0, description="Percentage of tokens pruned prior to inference")


class Diagnosis(BaseModel):
    """
    Master Diagnosis contract returned by the V.E.R.D.A.N.T. Multimodal Reasoning Engine.
    Strictly covers all 5 operational paths without synthetic mocks.
    """
    action_type: ActionType = Field(..., description="Selected operational path: advise, fix, test, env, clarify")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Model confidence score between 0.0 and 1.0")
    spoken_summary: str = Field(..., description="Concise 1-2 sentence spoken explanation for voice feedback")
    root_cause: str = Field(..., description="In-depth technical root cause analysis")
    evidence: Evidence = Field(default_factory=Evidence, description="Grounding evidence from logs, screens, and AST")
    edits: List[Edit] = Field(default_factory=list, description="List of atomic search/replace edits (for fix path)")
    test_spec: Optional[TestSpec] = Field(default=None, description="Synthesized reproducer test (for test or fix path)")
    env_action: Optional[EnvAction] = Field(default=None, description="1-Click environment command (for env path)")
    clarification_question: Optional[str] = Field(default=None, description="Follow-up question (for clarify path)")
    eco_audit: Optional[EcoAudit] = Field(default=None, description="Thermodynamic telemetry ledger")
