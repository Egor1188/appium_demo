import allure
import pytest

from pages.main_page import MainPage
from pages.views_page import ViewsPage


@allure.feature("Main screen")
@pytest.mark.parametrize("category", MainPage.CATEGORIES)
def test_main_screen_shows_category(driver, category):
    MainPage(driver).check_category_shown(category)


@allure.feature("Navigation")
def test_open_views_shows_buttons_item(driver):
    MainPage(driver).open_category("Views")
    ViewsPage(driver).check_item_shown("Buttons")


@allure.feature("Navigation")
def test_back_returns_to_main_screen(driver):
    main = MainPage(driver)
    main.open_category("Views")
    main.back()
    main.check_category_shown("Views")
