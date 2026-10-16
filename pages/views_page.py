from pages.base_page import BasePage


class ViewsPage(BasePage):
    def check_item_shown(self, name: str):
        self.assert_visible(name)

    def open_item(self, name: str):
        self.tap(name)
