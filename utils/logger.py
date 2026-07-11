"""
utils/logger.py

Central logging utility for RealNut Intelligence.

Creates both console and file loggers.

Usage
-----
from utils.logger import get_logger

logger = get_logger(__name__)

logger.info("Application started.")
logger.warning("Missing optional column.")
logger.error("Import failed.")
"""

import logging

from config.settings import LOG_FILE


def get_logger(name: str) -> logging.Logger:
    """
    Returns a configured logger.

    Parameters
    ----------
    name : str
        Usually __name__

    Returns
    -------
    logging.Logger
    """

    logger = logging.getLogger(name)

    # Prevent duplicate handlers
    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # ==============================
    # Console Output
    # ==============================

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    # ==============================
    # File Output
    # ==============================

    file_handler = logging.FileHandler(
        LOG_FILE,
        encoding="utf-8"
    )

    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    logger.propagate = False

    return logger