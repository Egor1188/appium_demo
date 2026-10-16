from pages.base_page import BasePage


class ViewsPage(BasePage):
    def has_item(self, name: str) -> bool:
        return self.is_visible(name)

    def open_item(self, name: str):
        self.tap(name)
