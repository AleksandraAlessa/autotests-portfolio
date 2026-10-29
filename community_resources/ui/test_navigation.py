import allure
from playwright.sync_api import Page, expect


@allure.feature("Навигация")
@allure.story("FR-01: Пункт меню 'Полезные ресурсы'")
def test_menu_item_visible_for_guest(guest_page: Page):
    guest_page.goto("/")
    menu_item = guest_page.locator("text=Полезные ресурсы")
    expect(menu_item).to_be_visible()


@allure.feature("Навигация")
@allure.story("FR-02: Переход на страницу модуля")
def test_click_menu_opens_page(guest_page: Page):
    guest_page.goto("/")
    guest_page.locator("text=Полезные ресурсы").click()
    expect(guest_page).to_have_url("/community-resources")


@allure.feature("Навигация")
@allure.story("FR-03: Два таба в сайдбаре (гость)")
def test_both_tabs_visible_for_guest(guest_page: Page):
    """Гость видит оба таба в сайдбаре."""
    guest_page.goto("/community-resources")
    expect(guest_page.locator("text=Ресурсы из чата")).to_be_visible()
    expect(guest_page.locator("text=Карьерные сайты")).to_be_visible()


@allure.feature("Навигация")
@allure.story("FR-04: Переключение табов без перезагрузки")
def test_tabs_switch_without_reload(guest_page: Page):
    guest_page.goto("/community-resources")
    url_before = guest_page.url
    guest_page.locator("text=Карьерные сайты").click()
    expect(guest_page.locator("text=Карьерные сайты")).to_be_visible()
    assert guest_page.url == url_before, "URL изменился при переключении таба"