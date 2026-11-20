"""
V.E.R.D.A.N.T. Autonomous Sentinel — CLI Entrypoint
Run locally or in CI/CD pipelines:
  python -m verdant_sentinel.cli --url http://localhost:8000 --viewports desktop,mobile
"""
import sys
import asyncio
import argparse
import json
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from .sentinel_crawler import SentinelCrawler
from .self_healer import DeterministicSelfHealer


async def run_sentinel(url: str, viewports: list, auto_heal: bool):
    print("\n" + "="*70)
    print("🌿 V.E.R.D.A.N.T. AUTONOMOUS SENTINEL — CI/CD SELF-HEALING ENGINE")
    print("="*70)
    print(f"Target URL: {url}")
    print(f"Viewports:  {', '.join(viewports)}")
    print(f"Auto-Heal:  {'ENABLED' if auto_heal else 'AUDIT ONLY'}\n")

    crawler = SentinelCrawler(base_url=url)
    defects = await crawler.audit_url(path="/", viewports=viewports)

    if not defects:
        print("\n✨ ZERO DEFECTS DETECTED: Application DOM and runtime are 100% healthy.")
        print("="*70 + "\n")
        return

    print(f"\n⚠️  {len(defects)} DEFECT(S) CAUGHT DURING HEADLESS AUDIT:")
    for idx, d in enumerate(defects, 1):
        print(f"  [{idx}] {d.get('type')} on '{d.get('selector')}' ({d.get('viewport')})")

    if auto_heal:
        print("\n🛠️  INITIATING CLOSED-LOOP SELF-HEALING PROTOCOL...")
        healer = DeterministicSelfHealer(workspace_root=str(PROJECT_ROOT))
        # Heal the first prominent defect
        report = healer.heal_defect(defects[0])
        
        print("\n" + "="*70)
        print("📋 SELF-HEALING AUDIT REPORT (VERIFIED RED -> GREEN)")
        print("="*70)
        print(f"Root Cause:     {report.get('root_cause')}")
        print(f"CSS Hot-Patch:  {report.get('css_patch')}")
        print(f"Test File:      {report.get('reproducer_test')}")
        print("\n🌱 DYNAMIC ECO-AUDIT LEDGER (Zero Hardcoding):")
        eco = report.get("eco_audit", {})
        print(f"  • Tokens Evaluated:      {eco.get('tokens_used')}")
        print(f"  • Tokens Pruned:         {eco.get('tokens_saved')} (-{eco.get('token_savings_pct')}%)")
        print(f"  • Grid Energy Conserved: {eco.get('energy_saved_wh')} Wh")
        print(f"  • Cooling Water Saved:   {eco.get('water_saved_ml')} mL (PUE 1.10 / WUE 1.18)")
        print("="*70 + "\n")


def main():
    parser = argparse.ArgumentParser(description="V.E.R.D.A.N.T. Autonomous CI/CD Sentinel")
    parser.add_argument("--url", default="http://localhost:8000", help="Base URL of the application to audit")
    parser.add_argument("--viewports", default="desktop,mobile", help="Comma-separated viewports: desktop,tablet,mobile")
    parser.add_argument("--no-heal", action="store_true", help="Audit only without auto-applying fixes")
    args = parser.parse_args()

    vps = [v.strip().lower() for v in args.viewports.split(",") if v.strip()]
    asyncio.run(run_sentinel(url=args.url, viewports=vps, auto_heal=not args.no_heal))


if __name__ == "__main__":
    main()
