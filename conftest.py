import allure
import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options
from loguru import logger

from config.settings import load_settings
from core.devices import device_for_worker, system_port_for_worker
from core.logger import setup_logging


@pytest.fixture(scope="session", autouse=True)
def _logging(worker_id):
    setup_logging(worker_id)


@pytest.fixture(scope="session")
def settings():
    return load_settings()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Keep the test result on the item so fixtures can see if the test failed."""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)


@pytest.fixture
def driver(request, settings, worker_id):
    """One driver per test. Each xdist worker gets its own device and systemPort."""
    udid = device_for_worker(settings.devices, worker_id)
    port = system_port_for_worker(settings.base_system_port, worker_id)
    options = UiAutomator2Options()
    options.platform_name = "Android"
    options.automation_name = "UiAutomator2"
    options.udid = udid
    options.app = settings.app_path
    options.system_port = port
    options.new_command_timeout = 120
    options.no_reset = False
    logger.info("Start test {} on {} (systemPort {})", request.node.name, udid, port)
    drv = webdriver.Remote(settings.appium_url, options=options)
    yield drv
    failed = getattr(request.node, "rep_call", None) is not None and request.node.rep_call.failed
    logger.log("ERROR" if failed else "INFO", "Test {} {}", request.node.name,
               "FAILED" if failed else "finished")
    if failed:
        allure.attach(drv.get_screenshot_as_png(), name="screenshot_on_failure",
                      attachment_type=allure.attachment_type.PNG)
    drv.quit()
