import allure
from playwright.sync_api import Page, expect


@allure.feature("Создание")
@allure.story("FR-24: Гость не видит кнопку 'Добавить'")
def test_add_button_hidden_for_guest(guest_page: Page):
    guest_page.goto("/community-resources")
    expect(
        guest_page.locator("button:has-text('Добавить'), button:has-text('Создать')")
    ).to_be_hidden()


@allure.feature("Создание")
@allure.story("FR-23: Кнопка 'Добавить' видна участнику")
def test_add_button_visible_for_member(member_page: Page):
    member_page.goto("/community-resources")
    expect(
        member_page.locator("button:has-text('Добавить'), button:has-text('Создать')")
    ).to_be_visible()


@allure.feature("Создание")
@allure.story("FR-27: Валидация заголовка")
def test_validation_title_required(member_page: Page):
    member_page.goto("/community-resources")
    member_page.locator("button:has-text('Добавить'), button:has-text('Создать')").click()
    member_page.locator("input[name='url']").fill("https://example.com")
    member_page.locator("button:has-text('Сохранить')").click()
    expect(member_page.locator("text=Заголовок обязателен")).to_be_visible()


@allure.feature("Создание")
@allure.story("FR-28: Валидация URL")
def test_validation_url_format(member_page: Page):
    member_page.goto("/community-resources")
    member_page.locator("button:has-text('Добавить'), button:has-text('Создать')").click()
    member_page.locator("input[name='title']").fill("Test")
    member_page.locator("input[name='url']").fill("abc")
    member_page.locator("button:has-text('Сохранить')").click()
    expect(member_page.locator("text=Введите корректный URL")).to_be_visible()


@allure.feature("Удаление")
@allure.story("FR-36: Участник не видит кнопку удаления")
def test_delete_button_hidden_for_member(member_page: Page):
    member_page.goto("/community-resources")
    expect(member_page.locator("button[aria-label='Удалить']")).to_have_count(0)
