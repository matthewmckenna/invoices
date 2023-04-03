from __future__ import annotations

import json
import logging
import logging.config
from pathlib import Path

from .config import load_logging_config_dict
from .dates_times import ymdhms_now
from .iotools import ensure_path


def setup_logging(
    logger_name: str | None = "dev", *, config_filepath: Path | None = None
) -> logging.Logger:
    """Configure logging"""
    project_directory = Path(__file__).parent.parent.parent
    # print(f"project_directory: {project_directory}")

    if config_filepath is None:
        # set a default log config path
        config_filepath = project_directory / "config.toml"
    # print(f"config_filepath: {config_filepath}")

    logs_directory = ensure_path(project_directory / "logs")
    # print(f"logs_directory: {logs_directory}")

    logging_config = load_logging_config_dict(config_filepath)
    print(json.dumps(logging_config, indent=2))

    # update the log filepath
    timestamp = ymdhms_now()
    logging_config["handlers"]["file_handler"]["filename"] = (
        logs_directory / f"{timestamp}.log"
    ).as_posix()

    logging.config.dictConfig(logging_config)
    return logging.getLogger(logger_name)
