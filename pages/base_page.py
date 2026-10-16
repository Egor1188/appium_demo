from appium.webdriver.common.appiumby import AppiumBy
from loguru import logger
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class BasePage:
    def __init__(self, driver, timeout: int = 15):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def _by_accessibility_id(self, value):
        return (AppiumBy.ACCESSIBILITY_ID, value)

    def tap(self, accessibility_id: str):
        logger.info("Tap '{}'", accessibility_id)
        self.wait.until(EC.element_to_be_clickable(self._by_accessibility_id(accessibility_id))).click()

    def is_visible(self, accessibility_id: str) -> bool:
        try:
            self.wait.until(EC.visibility_of_element_located(self._by_accessibility_id(accessibility_id)))
            return True
        except Exception:
            return False

    def assert_visible(self, accessibility_id: str):
        logger.info("Check '{}' is visible", accessibility_id)
        assert self.is_visible(accessibility_id), f"'{accessibility_id}' is not visible on the screen"

    def back(self):
        logger.info("Press Back")
        self.driver.back()
