import logging
import logging.config
from pathlib import Path
from typing import Any

import tomllib

from invoicetool.config import Config
from invoicetool.dates_times import ymdhms_now
from invoicetool.iotools import pathify


def setup_logging(
    *,
    logger_name: str | None = "dev",
    config_filepath: Path | str | None = Config.default_config_filepath,
) -> logging.Logger:
    """Configure logging"""
    logging_config = load_logging_config_dict(config_filepath)
    logs_directory = pathify(Config.project_directory) / "logs"
    logging_config["handlers"]["file_handler"]["filename"] = (
        logs_directory / f"{ymdhms_now()}.log"
    ).as_posix()
    logging.config.dictConfig(logging_config)
    return logging.getLogger(logger_name)


def load_logging_config_dict(path: Path | str) -> dict[str, Any]:
    """Load a logging config file and return as a dict"""
    with open(path, "rb") as f:
        return tomllib.load(f)["log"]
