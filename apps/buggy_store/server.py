"""
Standalone Buggy Web Application: NovaMart Cloud Store
Completely independent from VERDANT. Contains real, live reproducible bugs
for genuine forensic detection and multimodal screen recording.

Run:
    python apps/buggy_store/server.py
Access at:
    http://localhost:5050
"""
import os
import sys
import json
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"

PORT = 5050


class BuggyStoreHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(STATIC_DIR), **kwargs)

    def do_GET(self):
        if self.path == "/" or self.path == "/index.html":
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            index_path = STATIC_DIR / "index.html"
            self.wfile.write(index_path.read_bytes())
            return

        elif self.path == "/api/inventory":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            data = [
                {"id": 1, "name": "AI Tensor Accelerator v4", "price": 1299.00, "category": "Hardware", "stock": 4},
                {"id": 2, "name": "Ultra-Low-Power Edge Node", "price": 449.00, "category": "IoT", "stock": 12},
                {"id": 3, "name": "Quantum Crypto Token Key", "price": 89.00, "category": "Security", "stock": 25},
            ]
            self.wfile.write(json.dumps(data).encode("utf-8"))
            return

        super().do_GET()

    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length).decode("utf-8") if content_length > 0 else ""

        # BUG 1: Coupon API crash (Throws 500 Internal Server Error)
        if self.path == "/api/coupon":
            try:
                payload = json.loads(body) if body else {}
                code = payload.get("code", "").upper().strip()
            except Exception:
                code = ""

            if code == "SAVE50" or code == "FAIL":
                # Simulated backend crash: ZeroDivisionError
                self.send_response(500)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                err_resp = {
                    "status": "error",
                    "error_code": "INTERNAL_SERVER_ERROR",
                    "exception": "ZeroDivisionError: float division by zero",
                    "file": "pricing_engine.py",
                    "line": 42,
                    "message": f"Fatal unhandled exception in pricing_engine.py: coupon code '{code}' caused denominator to evaluate to 0."
                }
                self.wfile.write(json.dumps(err_resp).encode("utf-8"))
                return
            else:
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"status": "success", "discount": 0.10, "message": "10% discount applied"}).encode("utf-8"))
                return

        # BUG 2: Checkout endpoint
        elif self.path == "/api/checkout":
            try:
                payload = json.loads(body) if body else {}
            except Exception:
                payload = {}

            # If cart has negative total or missing cartId, return 400 or 500
            total = payload.get("total", 0)
            if total <= 0:
                self.send_response(400)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"status": "error", "message": "Invalid transaction amount: Total cannot be zero or negative"}).encode("utf-8"))
                return

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "success", "order_id": "ORD-94821", "message": "Order placed successfully"}).encode("utf-8"))
            return

        self.send_response(404)
        self.end_headers()


def run():
    STATIC_DIR.mkdir(parents=True, exist_ok=True)
    server_address = ("127.0.0.1", PORT)
    httpd = HTTPServer(server_address, BuggyStoreHandler)
    print("=" * 65)
    print(f"🛒 NovaMart Buggy Web App running live on: http://127.0.0.1:{PORT}")
    print("   Completely standalone · Zero VERDANT mocks · Real live bugs")
    print("   Press Ctrl+C to terminate the server")
    print("=" * 65)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n🛒 Server stopped.")


if __name__ == "__main__":
    run()
