from pages.base_page import BasePage


class MainPage(BasePage):
    CATEGORIES = ("Accessibility", "Animation", "App", "Graphics", "Media", "Text", "Views")

    def open_category(self, name: str):
        self.tap(name)

    def has_category(self, name: str) -> bool:
        return self.is_visible(name)
