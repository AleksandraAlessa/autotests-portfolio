"""
API-тесты для auth-service.

Эндпоинты:
- POST /auth/login
- POST /auth/logout
- GET  /auth/me

Cookie: session_id (HttpOnly, Secure, SameSite=Lax)
Роли: guest, member, moderator, admin

Примечания:
- Регресс BUG-001: /auth/me возвращал 401 после успешного /auth/login.
  Покрытие: test_me_after_login_same_session, test_me_with_valid_cookie,
  test_full_auth_flow.
- Флаг Secure выставляется только для HTTPS. В local (HTTP) проверка
  Secure выполняется условно, чтобы тесты были переносимы между окружениями.
"""

import allure
import pytest
import requests
from config import API_BASE, USER_EMAIL, USER_PASSWORD
from shared.helpers.auth import login_headers


def _secure_required() -> bool:
    """Secure-флаг актуален только для HTTPS. В local (HTTP) не проверяется."""
    return API_BASE.startswith("https://")


# ============================================================================
# POST /auth/login
# ============================================================================
@allure.feature("Auth")
@allure.story("Login: успешный вход")
def test_login_success():
    """TC-AUTH-001: Успешный вход с валидными данными."""
    session = requests.Session()
    resp = session.post(
        f"{API_BASE}/auth/login",
        json={"login": USER_EMAIL, "password": USER_PASSWORD},
        headers=login_headers(),
    )

    assert resp.status_code == 204, f"Ожидался 204, получен {resp.status_code}"
    assert "session_id" in session.cookies, "Cookie session_id не установлена"

    set_cookie = resp.headers.get("Set-Cookie", "")
    assert "HttpOnly" in set_cookie, "Cookie без флага HttpOnly"
    assert "SameSite=Lax" in set_cookie, "Cookie без флага SameSite=Lax"
    if _secure_required():
        assert "Secure" in set_cookie, "Cookie без флага Secure (HTTPS)"


@allure.feature("Auth")
@allure.story("Login: неверный пароль")
def test_login_wrong_password():
    """TC-AUTH-002: Вход с неверным паролем отклоняется."""
    session = requests.Session()
    resp = session.post(
        f"{API_BASE}/auth/login",
        json={"login": USER_EMAIL, "password": "wrong_password_12345"},
        headers=login_headers(),
    )

    assert resp.status_code == 401, f"Ожидался 401, получен {resp.status_code}"
    assert "session_id" not in session.cookies, "Cookie не должна быть установлена"


@allure.feature("Auth")
@allure.story("Login: несуществующий логин")
def test_login_nonexistent_user():
    """TC-AUTH-003: Вход с несуществующим логином отклоняется."""
    session = requests.Session()
    resp = session.post(
        f"{API_BASE}/auth/login",
        json={"login": "nonexistent_user_12345", "password": "any_password"},
        headers=login_headers(),
    )

    assert resp.status_code == 401, f"Ожидался 401, получен {resp.status_code}"


# --- Баг валидации: пустой login, пустой password, нет body, невалидный JSON ---
# Возвращается 500 вместо 400. Заведена карточка BUG-001.
# После фикса валидации — снять xfail.

@pytest.mark.xfail(
    reason="BUG-001: пустой login возвращает 500 вместо 400",
    strict=True,
)
@allure.feature("Auth")
@allure.story("Login: пустой login")
def test_login_empty_login():
    """TC-AUTH-004: Вход с пустым полем login."""
    resp = requests.post(
        f"{API_BASE}/auth/login",
        json={"login": "", "password": USER_PASSWORD},
        headers=login_headers(),
    )

    assert resp.status_code == 400, f"Ожидался 400, получен {resp.status_code}"


@pytest.mark.xfail(
    reason="BUG-001: пустой password возвращает 500 вместо 400",
    strict=True,
)
@allure.feature("Auth")
@allure.story("Login: пустой password")
def test_login_empty_password():
    """TC-AUTH-005: Вход с пустым полем password."""
    resp = requests.post(
        f"{API_BASE}/auth/login",
        json={"login": USER_EMAIL, "password": ""},
        headers=login_headers(),
    )

    assert resp.status_code == 400, f"Ожидался 400, получен {resp.status_code}"


@pytest.mark.xfail(
    reason="BUG-001: запрос без body возвращает 500 вместо 400",
    strict=True,
)
@allure.feature("Auth")
@allure.story("Login: нет body")
def test_login_no_body():
    """TC-AUTH-006: Вход без тела запроса."""
    resp = requests.post(
        f"{API_BASE}/auth/login",
        headers=login_headers(),
    )

    assert resp.status_code == 400, f"Ожидался 400, получен {resp.status_code}"


@pytest.mark.xfail(
    reason="BUG-001: невалидный JSON возвращает 500 вместо 400",
    strict=True,
)
@allure.feature("Auth")
@allure.story("Login: невалидный JSON")
def test_login_invalid_json():
    """TC-AUTH-007: Вход с невалидным JSON."""
    resp = requests.post(
        f"{API_BASE}/auth/login",
        data='{"login": "user3", "password":',
        headers={**login_headers(), "Content-Type": "application/json"},
    )

    assert resp.status_code == 400, f"Ожидался 400, получен {resp.status_code}"


# ============================================================================
# GET /auth/me
# ============================================================================
@allure.feature("Auth")
@allure.story("Me: с валидной cookie")
def test_me_with_valid_cookie(auth_session):
    """TC-AUTH-008: Профиль текущего пользователя.

    Связано с регрессом BUG-001: /auth/me возвращал 401 после login.
    """
    resp = auth_session.get(f"{API_BASE}/auth/me")

    assert resp.status_code == 200, f"Ожидался 200, получен {resp.status_code}"
    data = resp.json()

    assert "id" in data, "В ответе нет поля id"
    assert "login" in data, "В ответе нет поля login"
    assert "role" in data, "В ответе нет поля role"
    assert data["login"] == USER_EMAIL, "Login не совпадает"


@allure.feature("Auth")
@allure.story("Me: без cookie")
def test_me_without_cookie():
    """TC-AUTH-009: Запрос профиля без авторизации."""
    resp = requests.get(f"{API_BASE}/auth/me")

    assert resp.status_code == 401, f"Ожидался 401, получен {resp.status_code}"


@allure.feature("Auth")
@allure.story("Me: невалидная cookie")
def test_me_with_invalid_cookie():
    """TC-AUTH-010: Запрос профиля с невалидной cookie."""
    resp = requests.get(
        f"{API_BASE}/auth/me",
        cookies={"session_id": "invalid_token_12345"},
    )

    assert resp.status_code == 401, f"Ожидался 401, получен {resp.status_code}"


# ----------------------------------------------------------------------------
# Регресс BUG-001
# ----------------------------------------------------------------------------
@allure.feature("Auth")
@allure.story("Регресс BUG-001: /auth/me после login")
def test_me_after_login_same_session():
    """BUG-001: /auth/me сразу после /auth/login в одной сессии.

    Шаги:
      1. POST /auth/login в новую сессию.
      2. GET  /auth/me в ту же сессию (та же cookie).

    Ожидание: 200 и данные пользователя.
    До фикса: 401 {"code": "unauthorized", "message": "Нужно войти."}.
    """
    session = requests.Session()

    login_resp = session.post(
        f"{API_BASE}/auth/login",
        json={"login": USER_EMAIL, "password": USER_PASSWORD},
        headers=login_headers(),
    )
    assert login_resp.status_code == 204, (
        f"Шаг 1 (login): ожидался 204, получен {login_resp.status_code}"
    )
    assert "session_id" in session.cookies, (
        "Шаг 1 (login): cookie session_id не установлена"
    )

    me_resp = session.get(f"{API_BASE}/auth/me")
    assert me_resp.status_code == 200, (
        f"Шаг 2 (me): BUG-001, ожидался 200, получен "
        f"{me_resp.status_code}: {me_resp.text}"
    )
    assert me_resp.json()["login"] == USER_EMAIL, "Login в ответе не совпадает"


# ============================================================================
# POST /auth/logout
# ============================================================================
@allure.feature("Auth")
@allure.story("Logout: успешный выход")
def test_logout_success():
    """TC-AUTH-012: Успешное завершение сессии.

    Использует собственную сессию, чтобы не ломать shared auth_session
    для последующих тестов.
    """
    session = requests.Session()

    login_resp = session.post(
        f"{API_BASE}/auth/login",
        json={"login": USER_EMAIL, "password": USER_PASSWORD},
        headers=login_headers(),
    )
    assert login_resp.status_code == 204, "Шаг 1: login не удался"
    assert "session_id" in session.cookies, "Cookie session_id не установлена"

    resp = session.post(f"{API_BASE}/auth/logout")

    assert resp.status_code == 204, f"Ожидался 204, получен {resp.status_code}"

    set_cookie = resp.headers.get("Set-Cookie", "")
    assert "session_id=" in set_cookie, "Cookie не сброшена"
    assert "Max-Age=0" in set_cookie, "Cookie не помечена на удаление"


# --- Баг logout без cookie: должен быть 401, приходит 204. Карточка BUG-002 ---
@pytest.mark.xfail(
    reason="BUG-002: logout без cookie возвращает 204 вместо 401",
    strict=True,
)
@allure.feature("Auth")
@allure.story("Logout: без cookie")
def test_logout_without_cookie():
    """TC-AUTH-013: Выход без авторизации."""
    resp = requests.post(f"{API_BASE}/auth/logout")

    assert resp.status_code == 401, f"Ожидался 401, получен {resp.status_code}"


# ============================================================================
# E2E: full flow
# ============================================================================
@allure.feature("Auth")
@allure.story("Full flow: login -> me -> logout -> me")
def test_full_auth_flow():
    """TC-AUTH-015: Полный цикл работы с сессией.

    Покрывает регресс BUG-001 на шаге 2.
    """
    session = requests.Session()

    # 1. Login
    login_resp = session.post(
        f"{API_BASE}/auth/login",
        json={"login": USER_EMAIL, "password": USER_PASSWORD},
        headers=login_headers(),
    )
    assert login_resp.status_code == 204, "Шаг 1: login не удался"

    # 2. Me
    me_resp = session.get(f"{API_BASE}/auth/me")
    assert me_resp.status_code == 200, (
        f"Шаг 2 (BUG-001): ожидался 200, получен {me_resp.status_code}"
    )
    assert me_resp.json()["login"] == USER_EMAIL

    # 3. Logout
    logout_resp = session.post(f"{API_BASE}/auth/logout")
    assert logout_resp.status_code == 204, "Шаг 3: logout не удался"

    # 4. Me после logout
    me_after = session.get(f"{API_BASE}/auth/me")
    assert me_after.status_code == 401, "Шаг 4: профиль доступен после logout"


# ============================================================================
# Проверка ролей
# ============================================================================
@allure.feature("Auth")
@allure.story("Роль: member")
def test_role_member(auth_session):
    """TC-AUTH-016: Участник видит роль member.

    Использует shared auth_session. Не ломать её в других тестах!
    """
    resp = auth_session.get(f"{API_BASE}/auth/me")

    assert resp.status_code == 200, f"Ожидался 200, получен {resp.status_code}"
    assert resp.json()["role"] == "member", (
        f"Ожидалась роль member, получена {resp.json()['role']}"
    )


# ============================================================================
# Проверка cookie (безопасность)
# ============================================================================
@allure.feature("Auth")
@allure.story("Cookie: HttpOnly")
def test_cookie_httponly():
    """TC-AUTH-019: Cookie сессии имеет флаг HttpOnly."""
    session = requests.Session()
    resp = session.post(
        f"{API_BASE}/auth/login",
        json={"login": USER_EMAIL, "password": USER_PASSWORD},
        headers=login_headers(),
    )

    set_cookie = resp.headers.get("Set-Cookie", "")
    assert "HttpOnly" in set_cookie, "Cookie без флага HttpOnly"


@allure.feature("Auth")
@allure.story("Cookie: Secure")
def test_cookie_secure():
    """TC-AUTH-020: Cookie сессии имеет флаг Secure (только для HTTPS)."""
    if not _secure_required():
        pytest.skip(f"Secure-флаг актуален только для HTTPS (API_BASE={API_BASE})")

    session = requests.Session()
    resp = session.post(
        f"{API_BASE}/auth/login",
        json={"login": USER_EMAIL, "password": USER_PASSWORD},
        headers=login_headers(),
    )

    set_cookie = resp.headers.get("Set-Cookie", "")
    assert "Secure" in set_cookie, "Cookie без флага Secure"


@allure.feature("Auth")
@allure.story("Cookie: SameSite=Lax")
def test_cookie_samesite_lax():
    """TC-AUTH-021: Cookie сессии имеет SameSite=Lax."""
    session = requests.Session()
    resp = session.post(
        f"{API_BASE}/auth/login",
        json={"login": USER_EMAIL, "password": USER_PASSWORD},
        headers=login_headers(),
    )

    set_cookie = resp.headers.get("Set-Cookie", "")
    assert "SameSite=Lax" in set_cookie, "Cookie без флага SameSite=Lax"


# ============================================================================
# Заглушки: ждут данных (учётки модератора/админа, истёкшая cookie)
# ============================================================================
@pytest.mark.skip(reason="Нужна учётка модератора")
@allure.feature("Auth")
@allure.story("Роль: moderator")
def test_role_moderator():
    """TC-AUTH-017: Модератор видит роль moderator."""
    ...


@pytest.mark.skip(reason="Нужна учётка админа")
@allure.feature("Auth")
@allure.story("Роль: admin")
def test_admin():
    """TC-AUTH-018: Администратор видит роль admin."""
    ...


@pytest.mark.skip(reason="Нужен способ получить истёкшую cookie")
@allure.feature("Auth")
@allure.story("Me: истёкшая cookie")
def test_me_expired_cookie():
    """TC-AUTH-011: Запрос профиля с истёкшей cookie."""
    ...