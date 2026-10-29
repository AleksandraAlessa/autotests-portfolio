import allure
import pytest
import requests
from config import API_BASE

@allure.feature("Community Resources")
@allure.story("Получение списка ресурсов")
@pytest.mark.api
@pytest.mark.smoke
def test_get_resources_returns_200():
    """Проверяет, что эндпоинт отдает 200 и список items."""
    resp = requests.get(f"{API_BASE}/community-resources")
    assert resp.status_code == 200, f"Ожидался 200, получен {resp.status_code}"
    data = resp.json()
    assert "items" in data, "В ответе нет поля items"
    assert isinstance(data["items"], list), "items должен быть списком"