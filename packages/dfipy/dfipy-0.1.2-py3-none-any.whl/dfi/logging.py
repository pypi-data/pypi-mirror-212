"""
Codebase logging methods.
"""
import logging
import os
import sys
from pathlib import Path
from time import gmtime

import coloredlogs

LOGGING_LEVELS = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
    "CRITICAL": logging.CRITICAL,
}


def get_logging_level() -> int:
    """Return the env variable LOGGING_LEVEL. If not defined return the defaul INFO."""
    logging_level_env = os.getenv("LOGGING_LEVEL")

    if logging_level_env in LOGGING_LEVELS.keys():
        return LOGGING_LEVELS[logging_level_env]
    return logging.INFO


def setup_logger(filename: str) -> logging.Logger:
    """Setup log - to be removed alongside with coloredlogs and to be left to developers."""
    filepath = Path(filename)
    if len(filepath.parts) > 1:  # only affects 1st party filenames not 3rd party
        filename = filepath.stem + filepath.suffix

    logging.basicConfig()
    logging.Formatter.converter = gmtime
    logger = logging.getLogger(name=filename)

    coloredlogs.install(logger=logger)
    logger.propagate = False

    message_format = "%(asctime)s.%(msecs)03d UTC [%(name)s] [%(process)d] %(levelname)s: %(message)s"
    coloredFormatter = coloredlogs.ColoredFormatter(
        fmt=message_format,
    )
    ch = logging.StreamHandler(stream=sys.stdout)
    ch.setFormatter(fmt=coloredFormatter)
    if logger.hasHandlers():
        logger.handlers = []
    logger.addHandler(hdlr=ch)
    logger.setLevel(level=get_logging_level())

    return logger
