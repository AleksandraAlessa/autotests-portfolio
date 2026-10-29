import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

import allure
import pytest
import requests
from urllib.parse import urlparse
from playwright.sync_api import Browser, Page
from config import API_BASE, BASE_URL, USER_EMAIL, USER_PASSWORD
from shared.helpers.auth import login_headers
from shared.fixtures.sessions import create_auth_session



# ============================================================================
# API-фикстуры
# ============================================================================

@pytest.fixture(scope="session")
def auth_session():
    """Сессия с авторизацией (member)."""
    return create_auth_session(USER_EMAIL, USER_PASSWORD)

@pytest.fixture(scope="session")
def moderator_session():
    """Сессия модератора. Skip, если нет данных в .env."""
    from config import MODERATOR_EMAIL, MODERATOR_PASSWORD
    if not MODERATOR_EMAIL or not MODERATOR_PASSWORD:
        pytest.skip("Нет данных модератора в .env")
    return create_auth_session(MODERATOR_EMAIL, MODERATOR_PASSWORD)


@pytest.fixture(scope="session")
def admin_session():
    """Сессия админа. Skip, если нет данных в .env."""
    from config import ADMIN_EMAIL, ADMIN_PASSWORD
    if not ADMIN_EMAIL or not ADMIN_PASSWORD:
        pytest.skip("Нет данных админа в .env")
    return create_auth_session(ADMIN_EMAIL, ADMIN_PASSWORD)

# ============================================================================
# UI-фикстуры
# ============================================================================

def _login_and_get_cookies(email: str, password: str) -> dict:
    """Логинится и возвращает cookies для браузера."""
    session = create_auth_session(email, password)
    return session.cookies.get_dict()


def _cookie_domain() -> str:
    return urlparse(BASE_URL).hostname


@pytest.fixture(scope="function")
def guest_page(browser: Browser) -> Page:
    """Страница для гостя."""
    context = browser.new_context(base_url=BASE_URL)
    page = context.new_page()
    yield page
    context.close()


@pytest.fixture(scope="function")
def member_page(browser: Browser) -> Page:
    """Страница для участника (member)."""
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

# ============================================================================
# Общее: логирование запросов в Allure
# ============================================================================

@pytest.fixture(scope="function", autouse=True)
def allure_log_requests():
    original_request = requests.Session.request

    def logged_request(self, method, url, *args, **kwargs):
        response = original_request(self, method, url, *args, **kwargs)

        headers = kwargs.get("headers", {})
        body = kwargs.get("json", "") or kwargs.get("data", "")
        allure.attach(
            f"{method.upper()} {url}\nHeaders: {headers}\nBody: {body}",
            name=f"Запрос {method.upper()}",
            attachment_type=allure.attachment_type.TEXT,
        )
        allure.attach(
            f"Status: {response.status_code}\nBody: {response.text[:2000]}",
            name=f"Ответ (статус {response.status_code})",
            attachment_type=allure.attachment_type.TEXT,
        )
        return response

    requests.Session.request = logged_request
    yield
    requests.Session.request = original_request

    