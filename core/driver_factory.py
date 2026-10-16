from appium import webdriver
from appium.options.android import UiAutomator2Options

from config.settings import Settings


def create_driver(settings: Settings, udid: str, system_port: int):
    options = UiAutomator2Options()
    options.platform_name = "Android"
    options.automation_name = "UiAutomator2"
    options.udid = udid
    options.app = settings.app_path
    options.system_port = system_port
    options.new_command_timeout = 120
    options.no_reset = False
    return webdriver.Remote(settings.appium_url, options=options)
