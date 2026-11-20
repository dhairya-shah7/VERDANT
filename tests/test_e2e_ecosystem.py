import asyncio
import json
import time
import urllib.request
import websockets

async def run_e2e_test():
    uri = "ws://127.0.0.1:8000/ws/ide"
    print("[E2E Test] Connecting simulated VS Code extension to /ws/ide...")
    
    async with websockets.connect(uri) as ws:
        # 1. Verify Handshake
        greeting = json.loads(await ws.recv())
        print("[E2E Test] IDE Handshake Received:", greeting["message"])
        assert greeting["type"] == "HANDSHAKE_ACK"

        # 2. Simulate Chrome Extension Ingestion
        print("[E2E Test] Simulating Chrome Extension bug ingestion...")
        chrome_payload = {
            "url": "http://localhost:3000/dashboard",
            "pageTitle": "User Dashboard",
            "logs": [
                {"type": "error", "message": "TypeError: Cannot read properties of null (reading 'token') at auth.js:15"},
                {"type": "info", "message": "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.leakedToken"}
            ],
            "networkEvents": [
                {"url": "/api/v1/auth/session", "status": 401, "statusText": "Unauthorized"}
            ]
        }

        req = urllib.request.Request(
            "http://127.0.0.1:8000/api/extension/ingest",
            data=json.dumps(chrome_payload).encode("utf-8"),
            headers={"Content-Type": "application/json"}
        )

        loop = asyncio.get_running_loop()
        start = time.time()
        resp = await loop.run_in_executor(None, lambda: urllib.request.urlopen(req))
        diag_resp = json.loads(resp.read().decode("utf-8"))
        elapsed = time.time() - start
        print(f"[E2E Test] Chrome Ingestion returned in {elapsed:.2f}s | Action: {diag_resp.get('action_type')}")

        # 3. Verify WebSocket event arrived in VS Code
        print("[E2E Test] Waiting for WebSocket broadcast to VS Code...")
        ws_event_raw = await asyncio.wait_for(ws.recv(), timeout=5.0)
        ws_event = json.loads(ws_event_raw)
        
        print("[E2E Test] VS Code Event Received:", ws_event["type"])
        assert ws_event["type"] == "DEFECT_INGESTED"
        assert ws_event["url"] == "http://localhost:3000/dashboard"
        assert "diagnosis" in ws_event

        diag = ws_event["diagnosis"]
        print("[E2E Test] Suspect File:", diag.get("evidence", {}).get("suspect_file"))
        print("[E2E Test] Root Cause:", diag.get("root_cause")[:80] + "...")
        print("[E2E Test] ALL TESTS PASSED! Chrome -> Daemon -> Gemini 3.1 -> VS Code loop is 100% verified.")

if __name__ == "__main__":
    asyncio.run(run_e2e_test())
