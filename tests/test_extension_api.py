import os
import sys
import json
import time
import urllib.request

payload = {
    "url": "http://localhost:5173/products",
    "pageTitle": "Store Products",
    "element": {
        "selector": "div.pricing-card > h3.plan-title",
        "parentSelector": "div.pricing-card",
        "textPreview": "Enterprise Platinum Plus Tier Subscription Plan Annual Billing",
        "geometry": {
            "width": 280,
            "height": 65,
            "scrollWidth": 420,
            "clientWidth": 280,
            "hasHorizontalOverflow": True,
            "hasVerticalOverflow": False
        },
        "computedStyles": {
            "display": "flex",
            "position": "relative",
            "overflow": "visible",
            "boxSizing": "border-box"
        },
        "htmlSnippet": "<div class=\"pricing-card\"><h3 class=\"plan-title\">Enterprise Platinum Plus Tier Subscription Plan Annual Billing</h3></div>"
    },
    "logs": [
        {"type": "warn", "message": "Auth token Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.sensitivePayload expires soon"}
    ],
    "networkEvents": []
}

req = urllib.request.Request(
    "http://127.0.0.1:8000/api/extension/ingest",
    data=json.dumps(payload).encode("utf-8"),
    headers={"Content-Type": "application/json"}
)

start = time.time()
try:
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode("utf-8"))
        elapsed = time.time() - start
        print(f"HTTP STATUS: {resp.status}")
        print(f"LATENCY: {elapsed:.2f}s")
        print(f"ACTION TYPE: {data.get('action_type')}")
        print(f"CONFIDENCE: {data.get('confidence')}")
        print(f"SPOKEN SUMMARY: {data.get('spoken_summary')}")
        print(f"CSS PATCH: {data.get('css_patch')}")
        print(f"ROOT CAUSE: {data.get('root_cause')}")
        print(f"EDITS: {len(data.get('edits', []))} edits synthesized")
        if data.get("test_spec"):
            print(f"TEST SPEC: {data['test_spec']['path']} ({data['test_spec']['runner']})")
except Exception as e:
    print(f"ERROR: {e}")
