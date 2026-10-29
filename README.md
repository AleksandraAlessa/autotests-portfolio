# QA Automation Framework: Web Hub

Фреймворк для автоматизации тестирования веб-хаба комьюнити (API + UI).

## 🛠 Стек технологий

- **Язык:** Python 3.13+
- **Тест-раннер:** Pytest
- **API-тесты:** Requests
- **UI-тесты:** Playwright
- **Отчётность:** Allure Report
- **Управление зависимостями:** pip / requirements.txt

## Архитектура проекта

Проект разделён по доменам (модулям) и уровням тестирования:

- `shared/` — общие хелперы (авторизация, API-клиент) и фикстуры (сессии).
- `community_resources/` — тесты модуля «Полезные ресурсы» (API + UI).
- `hub_home/` — UI-тесты для главной страницы (навигация, карточки сервисов).

В каждом модуле тесты разделены на `api/` и `ui/`.

## Как запустить

1. Клонировать репозиторий:

   ```bash
   git clone https://github.com/AleksandraAlessa/autotests-portfolio.git
   cd autotests-portfolio