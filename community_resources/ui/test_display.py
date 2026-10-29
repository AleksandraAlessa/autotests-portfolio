import allure
import pytest
from playwright.sync_api import Page, expect


@allure.feature("Отображение списка")
@allure.story("FR-05: Только плитки в первой волне")
def test_tiles_view_is_default(guest_page: Page):
    """Проверяет, что по умолчанию отображается плиточный вид."""
    guest_page.goto("/community-resources")
    expect(
        guest_page.locator("[data-testid='tiles-container']")
    ).to_be_visible()


@allure.feature("Отображение списка")
@allure.story("FR-08: Содержимое карточки")
def test_card_contains_all_elements(guest_page: Page):
    guest_page.goto("/community-resources")

    cards = guest_page.locator("[data-testid='resource-card']")
    if cards.count() == 0:
        pytest.skip("На странице нет ни одной карточки (возможно, пустой список)")

    card = cards.first
    expect(card.locator("[data-testid='card-title']")).to_be_visible()
    expect(card.locator("[data-testid='card-url']")).to_be_visible()
    expect(card.locator("[data-testid='card-author']")).to_be_visible()
    expect(card.locator("[data-testid='card-date']")).to_be_visible()
