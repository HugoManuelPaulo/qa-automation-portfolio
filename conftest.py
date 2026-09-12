import json
import threading
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

import pytest


USERS = [
    {"id": 1, "name": "Ana Silva", "role": "QA Engineer"},
    {"id": 2, "name": "Mark de Vries", "role": "Developer"},
]


class DemoHandler(SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        pass

    def _json(self, status, payload):
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == "/api/users":
            return self._json(200, {"data": USERS, "count": len(USERS)})
        if self.path.startswith("/api/users/"):
            try:
                user_id = int(self.path.rsplit("/", 1)[-1])
            except ValueError:
                return self._json(400, {"error": "Invalid user id"})
            user = next((item for item in USERS if item["id"] == user_id), None)
            return self._json(200, user) if user else self._json(404, {"error": "User not found"})
        return super().do_GET()

    def do_POST(self):
        if self.path != "/api/users":
            return self._json(404, {"error": "Route not found"})
        try:
            length = int(self.headers.get("Content-Length", "0"))
            payload = json.loads(self.rfile.read(length) or b"{}")
        except (ValueError, json.JSONDecodeError):
            return self._json(400, {"error": "Invalid JSON"})
        if not payload.get("name") or not payload.get("role"):
            return self._json(422, {"error": "name and role are required"})
        return self._json(201, {"id": 3, "name": payload["name"], "role": payload["role"]})


@pytest.fixture(scope="session")
def base_url():
    app_dir = Path(__file__).parent / "app"
    handler = partial(DemoHandler, directory=str(app_dir))
    server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    url = f"http://127.0.0.1:{server.server_port}"
    yield url
    server.shutdown()
    thread.join(timeout=5)


@pytest.fixture
def driver():
    from selenium import webdriver

    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1440,900")
    browser = webdriver.Chrome(options=options)
    yield browser
    browser.quit()

