import pytest

from config.settings import load_settings
from core.devices import device_for_worker, system_port_for_worker, worker_index


@pytest.mark.parametrize("worker_id, expected", [("master", 0), ("gw0", 0), ("gw3", 3)])
def test_worker_index(worker_id, expected):
    assert worker_index(worker_id) == expected


def test_unknown_worker_id_is_rejected():
    with pytest.raises(ValueError):
        worker_index("worker-1")


def test_each_worker_gets_its_own_device():
    devices = ("emulator-5554", "emulator-5556")
    assert device_for_worker(devices, "gw0") == "emulator-5554"
    assert device_for_worker(devices, "gw1") == "emulator-5556"


def test_more_workers_than_devices_fails_loudly():
    with pytest.raises(RuntimeError, match="no device"):
        device_for_worker(("emulator-5554",), "gw1")


def test_each_worker_gets_its_own_system_port():
    assert system_port_for_worker(8200, "gw0") == 8200
    assert system_port_for_worker(8200, "gw2") == 8202


def test_settings_defaults_and_overrides():
    s = load_settings({})
    assert s.devices == ("emulator-5554",) and s.appium_url.endswith(":4723")
    s = load_settings({"DEVICES": "a, b", "BASE_SYSTEM_PORT": "9000"})
    assert s.devices == ("a", "b") and s.base_system_port == 9000
