import json
import threading
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse
import pytest

USERS = [{"id": 1, "name": "Ana Silva", "role": "QA Engineer"}, {"id": 2, "name": "Mark de Vries", "role": "Developer"}]
PRODUCTS = [
    {"id": 1, "name": "Mechanical Keyboard", "category": "Accessories", "price": 89.99},
    {"id": 2, "name": "Wireless Mouse", "category": "Accessories", "price": 39.50},
    {"id": 3, "name": "USB-C Dock", "category": "Connectivity", "price": 74.00},
    {"id": 4, "name": "QA Handbook", "category": "Books", "price": 24.90},
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

    def _body(self):
        try:
            length = int(self.headers.get("Content-Length", "0"))
            return json.loads(self.rfile.read(length) or b"{}")
        except (ValueError, json.JSONDecodeError):
            return None

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == "/api/users":
            return self._json(200, {"data": USERS, "count": len(USERS)})
        if parsed.path.startswith("/api/users/"):
            try:
                user_id = int(parsed.path.rsplit("/", 1)[-1])
            except ValueError:
                return self._json(400, {"error": "Invalid user id"})
            user = next((item for item in USERS if item["id"] == user_id), None)
            return self._json(200, user) if user else self._json(404, {"error": "User not found"})
        if parsed.path == "/api/products":
            query = parse_qs(parsed.query).get("q", [""])[0].lower()
            products = [item for item in PRODUCTS if query in (item["name"] + " " + item["category"]).lower()]
            return self._json(200, {"data": products, "count": len(products)})
        if parsed.path.startswith("/api/products/"):
            try:
                product_id = int(parsed.path.rsplit("/", 1)[-1])
            except ValueError:
                return self._json(400, {"error": "Invalid product id"})
            product = next((item for item in PRODUCTS if item["id"] == product_id), None)
            return self._json(200, product) if product else self._json(404, {"error": "Product not found"})
        return super().do_GET()

    def do_POST(self):
        payload = self._body()
        if payload is None:
            return self._json(400, {"error": "Invalid JSON"})
        if self.path == "/api/users":
            if not payload.get("name") or not payload.get("role"):
                return self._json(422, {"error": "name and role are required"})
            return self._json(201, {"id": 3, "name": payload["name"], "role": payload["role"]})
        if self.path == "/api/orders":
            customer, items = payload.get("customer", {}), payload.get("items", [])
            if not all(customer.get(key) for key in ("name", "email", "address")) or not items:
                return self._json(422, {"error": "customer and items are required"})
            try:
                total = 0
                for item in items:
                    product = next((p for p in PRODUCTS if p["id"] == item["product_id"]), None)
                    quantity = int(item["quantity"])
                    if product is None or quantity < 1:
                        raise ValueError
                    total += product["price"] * quantity
            except (KeyError, TypeError, ValueError):
                return self._json(422, {"error": "Invalid order item"})
            return self._json(201, {"order_id": "QC-2026-001", "status": "confirmed", "total": round(total, 2)})
        return self._json(404, {"error": "Route not found"})

@pytest.fixture(scope="session")
def base_url():
    app_dir = Path(__file__).parent / "app"
    server = ThreadingHTTPServer(("127.0.0.1", 0), partial(DemoHandler, directory=str(app_dir)))
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    yield f"http://127.0.0.1:{server.server_port}"
    server.shutdown()
    thread.join(timeout=5)

@pytest.fixture
def driver(request):
    from selenium import webdriver
    options = webdriver.ChromeOptions()
    for argument in ("--headless=new", "--no-sandbox", "--disable-dev-shm-usage", "--window-size=1440,900"):
        options.add_argument(argument)
    browser = webdriver.Chrome(options=options)
    yield browser
    if getattr(request.node, "rep_call", None) and request.node.rep_call.failed:
        Path("screenshots").mkdir(exist_ok=True)
        browser.save_screenshot(f"screenshots/{request.node.name}.png")
    browser.quit()

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    setattr(item, "rep_" + report.when, report)
