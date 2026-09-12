import pytest
import requests


pytestmark = pytest.mark.api


def test_list_users_returns_expected_contract(base_url):
    response = requests.get(f"{base_url}/api/users", timeout=5)

    assert response.status_code == 200
    payload = response.json()
    assert payload["count"] == 2
    assert all({"id", "name", "role"} <= user.keys() for user in payload["data"])


def test_get_existing_user(base_url):
    response = requests.get(f"{base_url}/api/users/1", timeout=5)

    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": "Ana Silva", "role": "QA Engineer"}


def test_missing_user_returns_404(base_url):
    response = requests.get(f"{base_url}/api/users/999", timeout=5)

    assert response.status_code == 404
    assert response.json()["error"] == "User not found"


def test_create_user_returns_201(base_url):
    response = requests.post(
        f"{base_url}/api/users",
        json={"name": "Hugo Paulo", "role": "QA Automation Engineer"},
        timeout=5,
    )

    assert response.status_code == 201
    assert response.json()["id"] == 3
    assert response.json()["role"] == "QA Automation Engineer"


def test_create_user_validates_required_fields(base_url):
    response = requests.post(f"{base_url}/api/users", json={"name": "Hugo Paulo"}, timeout=5)

    assert response.status_code == 422
    assert response.json()["error"] == "name and role are required"

