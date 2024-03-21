import logging
import logging.config
from pathlib import Path
from typing import Any

import tomllib

from invoicetool.config import Config
from invoicetool.dates_times import ymdhms_now
from invoicetool.iotools import pathify


def get_logger(
    *,
    logger_name: str | None = "dev",
    config_filepath: Path | str | None = None,
) -> logging.Logger:
    """Configure logging"""
    _config = (
        Config.from_file(config_filepath)
        if config_filepath is not None
        else Config.default()
    )
    logging_config = load_logging_config_dict(
        config_filepath or _config._DEFAULT_CONFIG_PATH
    )
    logs_directory = pathify(_config.project_directory) / "logs"
    logging_config["handlers"]["file_handler"]["filename"] = (
        logs_directory / f"{ymdhms_now()}.log"
    ).as_posix()
    logging.config.dictConfig(logging_config)
    return logging.getLogger(logger_name)


def load_logging_config_dict(path: Path | str) -> dict[str, Any]:
    """Load a logging config file and return as a dict"""
    with open(path, "rb") as f:
        return tomllib.load(f)["log"]
