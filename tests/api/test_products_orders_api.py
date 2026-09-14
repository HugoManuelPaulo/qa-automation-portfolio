import pytest
import requests

pytestmark = pytest.mark.api

def test_list_products_returns_ecommerce_contract(base_url):
    response = requests.get(f"{base_url}/api/products", timeout=5)
    assert response.status_code == 200
    payload = response.json()
    assert payload["count"] == 4
    assert all({"id", "name", "category", "price"} <= product.keys() for product in payload["data"])

def test_products_can_be_filtered_by_query(base_url):
    response = requests.get(f"{base_url}/api/products", params={"q": "accessories"}, timeout=5)
    assert response.status_code == 200
    assert response.json()["count"] == 2

def test_missing_product_returns_404(base_url):
    response = requests.get(f"{base_url}/api/products/999", timeout=5)
    assert response.status_code == 404
    assert response.json() == {"error": "Product not found"}

def test_create_order_calculates_server_side_total(base_url):
    response = requests.post(f"{base_url}/api/orders", json={
        "customer": {"name": "Hugo Paulo", "email": "hugo@example.com", "address": "Purmerend"},
        "items": [{"product_id": 1, "quantity": 2}, {"product_id": 4, "quantity": 1}],
    }, timeout=5)
    assert response.status_code == 201
    assert response.json() == {"order_id": "QC-2026-001", "status": "confirmed", "total": 204.88}

@pytest.mark.parametrize("payload", [
    {"customer": {}, "items": [{"product_id": 1, "quantity": 1}]},
    {"customer": {"name": "Hugo", "email": "hugo@example.com", "address": "NL"}, "items": []},
    {"customer": {"name": "Hugo", "email": "hugo@example.com", "address": "NL"}, "items": [{"product_id": 999, "quantity": 1}]},
])
def test_order_validation_rejects_invalid_payloads(base_url, payload):
    response = requests.post(f"{base_url}/api/orders", json=payload, timeout=5)
    assert response.status_code == 422
