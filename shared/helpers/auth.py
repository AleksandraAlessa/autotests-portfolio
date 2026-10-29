from config import BASE_URL


def login_headers() -> dict:
    """Заголовки для запроса авторизации (Origin и Referer из BASE_URL)."""
    return {
        "Origin": BASE_URL,
        "Referer": f"{BASE_URL}/",
        "User-Agent": "Mozilla/5.0",
        "Content-Type": "application/json",
    }