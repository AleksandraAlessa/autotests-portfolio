"""
API-тесты для /health.

Эндпоинт: GET /health
Ответ: 200 + {"status": "ok"}
Без авторизации.
"""

import allure
import requests
from config import API_BASE


@allure.feature("Health")
@allure.story("Smoke: сервис доступен")
def test_health_returns_ok():
    """GET /health возвращает 200 и {"status": "ok"}."""
    resp = requests.get(f"{API_BASE}/health", timeout=5)

    assert resp.status_code == 200, f"Ожидался 200, получен {resp.status_code}"

    data = resp.json()
    assert "status" in data, "В ответе нет поля status"
    assert data["status"] == "ok", f"Ожидался status=ok, получен {data['status']}"


@allure.feature("Health")
@allure.story("Content-Type ответа")
def test_health_content_type():
    """GET /health возвращает JSON."""
    resp = requests.get(f"{API_BASE}/health", timeout=5)

    content_type = resp.headers.get("Content-Type", "")
    assert "application/json" in content_type, (
        f"Ожидался application/json, получен {content_type}"
    )