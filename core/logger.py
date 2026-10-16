"""Logging via loguru: console plus one log file per xdist worker."""
import sys

from loguru import logger

from config.settings import ROOT

_FORMAT = "{time:HH:mm:ss.SSS} | {level: <7} | {extra[worker]} | {message}"


def setup_logging(worker_id: str = "master") -> None:
    logger.remove()
    logger.configure(extra={"worker": worker_id})
    logger.add(sys.stderr, level="INFO", format=_FORMAT)
    logger.add(ROOT / "logs" / f"test_{worker_id}.log", level="DEBUG", format=_FORMAT,
               mode="w", enqueue=True)
