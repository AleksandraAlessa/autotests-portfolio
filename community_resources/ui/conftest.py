"""Фикстуры для UI-тестов модуля community_resources."""
import pytest
import requests
from urllib.parse import urlparse

from playwright.sync_api import Browser, Page

from config import API_BASE, BASE_URL, USER_EMAIL, USER_PASSWORD
from shared.helpers.auth import login_headers


def _login_and_get_cookies(email: str, password: str) -> dict:
    """Логинится через API и возвращает cookies для передачи в браузер."""
    session = requests.Session()
    resp = session.post(
        f"{API_BASE}/auth/login",
        json={"login": email, "password": password},
        headers=login_headers(),
    )
    assert resp.status_code in (200, 204), f"Логин не удался: {resp.status_code}"
    return session.cookies.get_dict()


def _cookie_domain() -> str:
    """Извлекает домен из BASE_URL для установки cookies в браузере."""
    return urlparse(BASE_URL).hostname


@pytest.fixture(scope="function")
def guest_page(browser: Browser) -> Page:
    """Страница для гостя (без авторизации)."""
    context = browser.new_context(base_url=BASE_URL)
    page = context.new_page()
    yield page
    context.close()


@pytest.fixture(scope="function")
def member_page(browser: Browser) -> Page:
    """Страница для авторизованного участника (member)."""
    context = browser.new_context(base_url=BASE_URL)
    cookies = _login_and_get_cookies(USER_EMAIL, USER_PASSWORD)
    domain = _cookie_domain()
    context.add_cookies([
        {"name": k, "value": v, "domain": domain, "path": "/"}
        for k, v in cookies.items()
    ])
    page = context.new_page()
    yield page
    context.close()