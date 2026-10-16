from pages.base_page import BasePage


class MainPage(BasePage):
    CATEGORIES = ("Accessibility", "Animation", "App", "Graphics", "Media", "Text", "Views")

    def open_category(self, name: str):
        self.tap(name)

    def check_category_shown(self, name: str):
        self.assert_visible(name)
