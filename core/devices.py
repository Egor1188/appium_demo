"""Device allocation for parallel runs (pytest-xdist): one device per worker."""


def worker_index(worker_id: str) -> int:
    """'master' (no xdist) -> 0, 'gw0' -> 0, 'gw3' -> 3."""
    if worker_id == "master":
        return 0
    if worker_id.startswith("gw") and worker_id[2:].isdigit():
        return int(worker_id[2:])
    raise ValueError(f"Unknown xdist worker id: {worker_id!r}")


def device_for_worker(devices: tuple, worker_id: str) -> str:
    idx = worker_index(worker_id)
    if idx >= len(devices):
        raise RuntimeError(
            f"Worker {worker_id} has no device: {len(devices)} device(s) configured. "
            f"Run with -n <= {len(devices)} or add UDIDs to DEVICES."
        )
    return devices[idx]


def system_port_for_worker(base_port: int, worker_id: str) -> int:
    return base_port + worker_index(worker_id)
