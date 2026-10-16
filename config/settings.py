"""Settings come from environment variables, so the same code runs locally and in CI."""
import os
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class Settings:
    appium_url: str
    app_path: str
    devices: tuple          # UDIDs, e.g. ("emulator-5554", "emulator-5556")
    base_system_port: int   # each parallel worker needs its own UiAutomator2 systemPort
    wait_timeout: int


def load_settings(env=None) -> Settings:
    env = os.environ if env is None else env
    devices = tuple(d.strip() for d in env.get("DEVICES", "emulator-5554").split(",") if d.strip())
    return Settings(
        appium_url=env.get("APPIUM_URL", "http://127.0.0.1:4723"),
        app_path=env.get("APP_PATH", str(ROOT / "apps" / "ApiDemos-debug.apk")),
        devices=devices,
        base_system_port=int(env.get("BASE_SYSTEM_PORT", "8200")),
        wait_timeout=int(env.get("WAIT_TIMEOUT", "15")),
    )
