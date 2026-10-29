import requests

from config import BASE_URL


def test_homepage_returns_html():
    """Smoke: главная страница доступна и отдаёт HTML."""
    resp = requests.get(BASE_URL, timeout=5)
    assert resp.status_code == 200, f"Ожидался 200, получен {resp.status_code}"
    assert resp.headers.get("content-type", "").startswith("text/html"), (
        "Главная страница должна отдавать HTML"
    )
    assert "<html" in resp.text.lower(), "В ответе нет HTML-разметки"
