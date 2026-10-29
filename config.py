import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL")
API_BASE = os.getenv("API_BASE")

if not BASE_URL or not API_BASE:
    raise RuntimeError(
        "Не заданы BASE_URL и API_BASE. "
        "Создайте .env на основе .env.example"
    )

USER_EMAIL = os.getenv("USER_EMAIL")
USER_PASSWORD = os.getenv("USER_PASSWORD")
MODERATOR_EMAIL = os.getenv("MODERATOR_EMAIL")
MODERATOR_PASSWORD = os.getenv("MODERATOR_PASSWORD")
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")