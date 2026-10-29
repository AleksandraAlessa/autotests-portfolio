import allure
from playwright.sync_api import Page, expect


@allure.feature("Поиск")
@allure.story("FR-13: Поиск по названию")
def test_search_by_title(guest_page: Page):
    guest_page.goto("/community-resources")
    search = guest_page.locator("input[type='search'], input[placeholder*='Поиск']")
    search.fill("React")
    guest_page.keyboard.press("Enter")
    guest_page.wait_for_timeout(1000)

    cards = guest_page.locator("[data-testid='resource-card']")
    for i in range(cards.count()):
        text = cards.nth(i).inner_text()
        assert "react" in text.lower(), f"Карточка не содержит 'React': {text}"


@allure.feature("Фильтры")
@allure.story("FR-17: Блок фильтров")
def test_filters_block_visible(guest_page: Page):
    guest_page.goto("/community-resources")
    expect(guest_page.locator("[data-testid='filter-tags']")).to_be_visible()
    expect(guest_page.locator("[data-testid='filter-author']")).to_be_visible()
    expect(guest_page.locator("[data-testid='filter-date-from']")).to_be_visible()
    expect(guest_page.locator("[data-testid='filter-date-to']")).to_be_visible()


@allure.feature("Фильтры")
@allure.story("FR-18: Набор тегов не фиксирован")
def test_tags_filter_dynamic(guest_page: Page):
    """Проверяет, что фильтр тегов содержит хотя бы один тег."""
    guest_page.goto("/community-resources")
    guest_page.locator("[data-testid='filter-tags']").click()
    options = guest_page.locator("[data-testid='filter-tags'] option")
    assert options.count() > 0, "В фильтре тегов нет ни одного тега"