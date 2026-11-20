# 🌿 V.E.R.D.A.N.T. Autonomous Sentinel (CI/CD)

> **Headless Self-Healing Synthetic Test Runner for Modern Web Applications**

Part of the **V.E.R.D.A.N.T. Trinity**:
- `verdant-chrome/` — Interactive In-Browser Developer Cockpit
- `verdant-vscode/` — Real-Time Local IDE Bridge
- `verdant-sentinel/` — Autonomous Headless CI/CD Self-Healing Runner

---

## ⚡ What It Does

1. **Synthetic Ghost User Crawl**: Launches headless Playwright across multiple responsive viewports (Desktop `1920x1080`, Mobile `375x667`).
2. **Mathematical Defect Detection**: Intercepts console errors, HTTP 4xx/5xx drops, and computed layout overflows (`scrollWidth > clientWidth`).
3. **ContextPrism Dynamic AST/DOM Pruning**: Strips boilerplate and non-semantic markup to eliminate token bloat prior to LLM reasoning.
4. **Deterministic RED -> GREEN Proof**:
   - Synthesizes an executable Playwright test (`test_sentinel_reproducer.py`).
   - Asserts failure on unpatched code (RED ❌).
   - Applies atomic Search/Replace patch to source code.
   - Re-asserts pass on patched code (GREEN ✅).
5. **Real-Time Eco-Audit Ledger**: Computes genuine energy (Wh) and cooling water (mL) savings using Google Cloud PUE 1.10 and WUE 1.18 L/kWh standards.

---

## 🚀 Running the Sentinel Locally

```powershell
# Run the autonomous audit and self-heal against your running application:
python -m verdant-sentinel.cli --url http://localhost:8000 --viewports desktop,mobile

# Run audit only without modifying source files:
python -m verdant-sentinel.cli --url http://localhost:8000 --no-heal
```

---

## 🔄 GitHub Actions Integration

Drop `workflows/verdant_sentinel.yml` into your repository's `.github/workflows/` directory to automatically catch regressions and commit verified fixes on every pull request.
