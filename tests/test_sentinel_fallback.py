import io
import json
import os
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "verdant-sentinel"))

from self_healer import DeterministicSelfHealer


class FakeResponse(io.BytesIO):
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        self.close()


def test_heal_defect_succeeds_without_gemini_key(monkeypatch, tmp_path):
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)

    def fake_urlopen(request, timeout):
        payload = {
            "confidence": 0.95,
            "spoken_summary": "Cloud fallback diagnosis.",
            "root_cause": "Horizontal overflow detected.",
            "evidence": {"suspect_file": "src/stitch_template.py"},
            "css_patch": ".overflow-target { overflow: hidden; }",
            "edits": [],
            "eco_audit": {
                "tokens_used": 350,
                "energy_wh": 0.02,
                "water_ml": 0.01,
                "energy_saved_wh": 0.8,
                "water_saved_ml": 0.6,
                "compression_ratio_pct": 75.0,
            },
        }
        return FakeResponse(json.dumps(payload).encode("utf-8"))

    import urllib.request

    monkeypatch.setattr(urllib.request, "urlopen", fake_urlopen)

    healer = DeterministicSelfHealer(workspace_root=str(tmp_path))
    report = healer.heal_defect(
        {
            "type": "LAYOUT_OVERFLOW",
            "selector": ".overflow-target",
            "url": "https://example.com",
            "viewport": "mobile",
            "geometry": {
                "overflowPixels": 24,
                "clientWidth": 375,
                "scrollWidth": 399,
            },
            "computedStyles": {},
            "htmlSnippet": "<div class='overflow-target'>Overflow</div>",
            "tagName": "div",
            "textPreview": "Overflow",
        }
    )

    assert report["status"] == "SELF_HEALED"
    assert report["root_cause"] == "Horizontal overflow detected."
    assert report["css_patch"] == ".overflow-target { overflow: hidden; }"
    assert os.getenv("GEMINI_API_KEY") is None
