# Appium demo (Android, Python)

A small test framework that shows how I structure mobile automation: pytest, Appium 2
(UiAutomator2), Page Object, Allure reports with a screenshot on failure, and parallel runs
on several devices with pytest-xdist. It tests the public **ApiDemos** sample app, so it contains
no code or data from any employer.

## Structure
```
config/settings.py      settings from environment variables (no hard-coded values)
core/driver_factory.py  creates the Appium driver
core/devices.py         one device and one systemPort per xdist worker
pages/                  Page Objects (BasePage with explicit waits, MainPage, ViewsPage)
tests/conftest.py       driver fixture, screenshot attached to Allure on failure
tests/ui/               UI tests (marker: device)
tests/unit/             tests of the framework itself, run without a device
```

## Setup
1. Install JDK 17, Android Studio (SDK + emulator), Node.js. Set `ANDROID_HOME`.
2. `npm install -g appium` and `appium driver install uiautomator2`
3. `pip install -r requirements.txt` (or `poetry install`)
4. Put `ApiDemos-debug.apk` into `apps/` (see `apps/README.md`).
5. Start an emulator and check `adb devices`.

## Run
```bash
appium                                   # terminal 1
pytest -m "not device" -v                # framework unit tests, no device needed
pytest -m device -v --alluredir=allure-results      # UI tests on one device
DEVICES=emulator-5554,emulator-5556 pytest -m device -n 2   # two devices in parallel
allure serve allure-results              # report (Allure CLI required)
```

## Settings (environment variables)
`APPIUM_URL` (default `http://127.0.0.1:4723`), `APP_PATH`, `DEVICES` (comma-separated UDIDs),
`BASE_SYSTEM_PORT` (default 8200), `WAIT_TIMEOUT` (default 15).

## Design notes
- Explicit waits only (`WebDriverWait`), no `sleep`.
- With `-n N` every worker takes its own device from `DEVICES` and its own `systemPort`
  (`BASE_SYSTEM_PORT + worker index`), so parallel sessions do not collide. If there are more
  workers than devices, the run fails with a clear message.
- The device tests are separated by the `device` marker, so CI can run the framework tests anywhere.
