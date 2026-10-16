# Appium demo (Android, Python)

A small UI test framework for Android that shows how mobile automation can be structured:
**pytest**, **Appium 2** (UiAutomator2), **Page Object**, **Allure** reports with a screenshot on
failure, **loguru** logging, and parallel runs on several devices with **pytest-xdist**.

The tests run against the public **ApiDemos** sample app from the Appium docs.

## What the tests check
- The main screen shows every category (Accessibility, Animation, App, Graphics, Media, Text, Views).
- Opening **Views** shows the *Buttons* item.
- Pressing Back from **Views** returns to the main screen.

## Project structure
```
conftest.py             fixtures: settings, logging, Appium driver, Allure screenshot on failure
config/settings.py      settings from environment variables (no hard-coded values)
core/devices.py         one device and one systemPort per xdist worker
core/logger.py          loguru setup: console + logs/test_<worker>.log
pages/                  Page Objects: BasePage (waits, taps, checks), MainPage, ViewsPage
tests/ui/               UI tests
apps/                   put ApiDemos-debug.apk here (see apps/README.md)
```

## How it works
- **Driver** is created in the `driver` fixture in `conftest.py`, one per test, and closed after it.
  On failure a screenshot is attached to the Allure report.
- **Page Objects** hold locators, actions, explicit waits and **all assertions**
  (`check_*` methods). Tests only call page methods and contain no `assert`.
- **Parallel runs:** with `-n N` every worker takes its own device from `DEVICES` and its own
  `systemPort` (`BASE_SYSTEM_PORT + worker index`), so sessions do not collide. If there are more
  workers than devices, the run fails with a clear message.
- **Logging:** each action (tap, check, back) and the start/end of each test are logged to the
  console and to `logs/test_<worker>.log`.

## Requirements
Python 3.10+, JDK 17, Android SDK with an emulator (Android Studio), Node.js, Appium 2.

## Setup
1. Install JDK 17, Android Studio (SDK + emulator), Node.js. Set `ANDROID_HOME`.
2. `npm install -g appium` and `appium driver install uiautomator2`
3. `pip install -r requirements.txt` (or `poetry install`)
4. Put `ApiDemos-debug.apk` into `apps/`.
5. Start an emulator and check `adb devices`.

## Run
```bash
appium                                              # terminal 1
pytest -v --alluredir=allure-results                # terminal 2: one device
DEVICES=emulator-5554,emulator-5556 pytest -n 2     # two devices in parallel
allure serve allure-results                         # report (Allure CLI required)
```

## Settings (environment variables)
| Variable | Default | Meaning |
|---|---|---|
| `APPIUM_URL` | `http://127.0.0.1:4723` | Appium server address |
| `APP_PATH` | `apps/ApiDemos-debug.apk` | path to the app under test |
| `DEVICES` | `emulator-5554` | comma-separated device UDIDs |
| `BASE_SYSTEM_PORT` | `8200` | first UiAutomator2 `systemPort`; each worker adds its index |
