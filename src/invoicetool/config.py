from __future__ import annotations

import json
import tomllib
from dataclasses import dataclass
from pathlib import Path
from typing import Any, TypeVar

T = TypeVar("T")


@dataclass
class Config:
    extensions: list[int]
    database_path: Path
    # log_config: LogConfig

    def __post_init__(self):
        self.database_path = Path(self.database_path).expanduser()


# @dataclass
# class LoggingConfig:
#     version: int
#     disable_existing_loggers: bool
#     formatters: dict[str, dict[str, str]]
#     handlers: dict[str, dict[str, str]]
#     loggers: dict[str, dict[str, str]]
#     root: dict[str, str]

#     @classmethod
#     def from_dict(cls: T, config_dict: dict[str, Any]) -> T:
#         return cls(**config_dict)

# @dataclass
# class LogConfig:
#     version: int
#     disable_existing_loggers: bool
#     formatters: dict[str, dict[str, str]]
#     handlers: dict[str, dict[str, str]]
#     loggers: dict[str, dict[str, str]]
#     root: dict[str, str]


def load_config_dict(filepath: Path | str) -> dict[str, Any]:
    """Load a config file and return as a dict"""
    if isinstance(filepath, str):
        filepath = Path(filepath)
    with open(filepath, "rb") as f:
        if filepath.suffix == ".toml":
            config_dict = tomllib.load(f)
        elif filepath.suffix == ".json":
            config_dict = json.load(f)
        else:
            raise ValueError(f"Unsupported file format: {filepath.suffix}")
    return config_dict


def load_logging_config_dict(filepath: Path | str) -> dict[str, Any]:
    """Load a logging config file and return as a dict"""
    config_dict = load_config_dict(filepath)
    return config_dict["log"]


def load_logging_config(filepath: Path | str) -> LoggingConfig:
    """Load a logging config file and return as a dict"""
    logging_config_dict = load_logging_config_dict(filepath)
    return LoggingConfig.from_dict(logging_config_dict)
