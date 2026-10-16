import allure
import pytest

from pages.main_page import MainPage
from pages.views_page import ViewsPage

pytestmark = pytest.mark.device


@allure.feature("Main screen")
@pytest.mark.parametrize("category", MainPage.CATEGORIES)
def test_main_screen_shows_category(driver, category):
    assert MainPage(driver).has_category(category)


@allure.feature("Navigation")
def test_open_views_shows_buttons_item(driver):
    MainPage(driver).open_category("Views")
    assert ViewsPage(driver).has_item("Buttons")


@allure.feature("Navigation")
def test_back_returns_to_main_screen(driver):
    main = MainPage(driver)
    main.open_category("Views")
    main.back()
    assert main.has_category("Views")
