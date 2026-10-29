"""
Хелперы для создания авторизованных сессий.

Используются в conftest.py для фикстур auth_session, moderator_session, admin_session.

"""

import requests
from config import API_BASE
from shared.helpers.auth import login_headers


def create_auth_session(login: str, password: str) -> requests.Session:
    """
    Создаёт авторизованную сессию.

    Логинится через POST /auth/login, сохраняет cookie session_id
    в requests.Session и возвращает её.

    :param login: логин пользователя
    :param password: пароль
    :return: requests.Session с установленной cookie
    :raises AssertionError: если логин не удался
    """
    session = requests.Session()
    resp = session.post(
        f"{API_BASE}/auth/login",
        json={"login": login, "password": password},
        headers=login_headers(),
    )
    assert resp.status_code == 204, (
        f"Логин не удался для {login}: получен {resp.status_code}"
    )
    return session