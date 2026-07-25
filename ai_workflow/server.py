from __future__ import annotations

import json
import os
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from typing import Any

# Ensure parent directory is in sys.path
sys.path.insert(0, str(Path(__file__).parent))

from app.local_parser import parse_known_demo
from app.orchestrator import run_guidance
from app.schemas import StudentProfile


class GuidanceAPIHandler(BaseHTTPRequestHandler):
    def _set_cors_headers(self) -> None:
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def do_OPTIONS(self) -> None:
        self.send_response(200)
        self._set_cors_headers()
        self.end_headers()

    def do_GET(self) -> None:
        if self.path == "/api/health":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self._set_cors_headers()
            self.end_headers()
            self.wfile.write(json.dumps({"status": "ok", "message": "Guidance Engine API running"}).encode("utf-8"))
            return

        if self.path == "/api/sample-personas":
            personas = {
                "class10": parse_known_demo("class10").model_dump(),
                "class12": parse_known_demo("class12").model_dump(),
                "class12_arts": parse_known_demo("class12_arts").model_dump(),
                "aryan": parse_known_demo("aryan").model_dump(),
                "dashboard": parse_known_demo("dashboard").model_dump(),
                "ux": parse_known_demo("ux").model_dump(),
            }
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self._set_cors_headers()
            self.end_headers()
            self.wfile.write(json.dumps(personas).encode("utf-8"))
            return

        self.send_response(404)
        self.end_headers()

    def do_POST(self) -> None:
        if self.path == "/api/guidance":
            content_length = int(self.headers.get("Content-Length", 0))
            body_bytes = self.rfile.read(content_length)
            try:
                data: dict[str, Any] = json.loads(body_bytes.decode("utf-8"))
            except Exception:
                self.send_response(400)
                self._set_cors_headers()
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Invalid JSON payload"}).encode("utf-8"))
                return

            try:
                if "preset" in data:
                    profile = parse_known_demo(data["preset"])
                elif "profile" in data:
                    profile = StudentProfile.model_validate(data["profile"])
                else:
                    self.send_response(400)
                    self._set_cors_headers()
                    self.end_headers()
                    self.wfile.write(json.dumps({"error": "Payload must contain 'preset' or 'profile'"}).encode("utf-8"))
                    return

                result = run_guidance(profile)
                output = result.model_dump()

                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self._set_cors_headers()
                self.end_headers()
                self.wfile.write(json.dumps(output).encode("utf-8"))
            except Exception as err:
                self.send_response(500)
                self.send_header("Content-Type", "application/json")
                self._set_cors_headers()
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(err)}).encode("utf-8"))
            return

        self.send_response(404)
        self.end_headers()


def run_server(port: int = 8000) -> None:
    server_address = ("", port)
    httpd = HTTPServer(server_address, GuidanceAPIHandler)
    print(f"Server running on http://localhost:{port}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server.")
        httpd.server_close()


if __name__ == "__main__":
    port = int(os.getenv("PORT", "8000"))
    run_server(port)
