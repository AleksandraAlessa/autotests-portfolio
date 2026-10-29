import allure
import pytest
from playwright.sync_api import Page, expect
from config import BASE_URL


@allure.feature("Вёрстка")
@allure.story("Layout: mainInner растягивается на всю высоту main")
def test_main_inner_takes_full_height(page: Page):
    """Проверяет, что mainInner (div с h-full) имеет ту же высоту, что и <main>."""
    page.goto(BASE_URL)

    main_locator = page.locator("main")
    main_inner_locator = page.locator("main > div.h-full").first

    expect(main_locator).to_be_visible()
    expect(main_inner_locator).to_be_visible()

    main_box = main_locator.bounding_box()
    inner_box = main_inner_locator.bounding_box()

    assert main_box is not None, "Не удалось получить размеры <main>"
    assert inner_box is not None, "Не удалось получить размеры mainInner"

    main_height = main_box["height"]
    inner_height = inner_box["height"]

    allure.attach(
        f"Высота <main>: {main_height}px\nВысота mainInner: {inner_height}px",
        name="Замеры высоты",
        attachment_type=allure.attachment_type.TEXT,
    )

    assert abs(main_height - inner_height) <= 1, (
        f"mainInner ({inner_height}px) не растягивается на всю высоту "
        f"<main> ({main_height}px). Разница: {abs(main_height - inner_height)}px"
    )