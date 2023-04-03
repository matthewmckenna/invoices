from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .config import Config, load_config


@dataclass
class FormatterConfig:
    format: str


@dataclass
class StreamHandlerConfig:
    class_: str
    level: str
    formatter: str
    stream: str


@dataclass
class FileHandlerConfig:
    class_: str
    # level: str
    formatter: str
    filename: str
    mode: str
    encoding: str


@dataclass
class LoggerConfig:
    level: str
    handlers: list[str]
    propagate: bool


@dataclass
class LoggingConfig:
    formatters: dict[str, FormatterConfig]
    handlers: dict[str, dict[str, str]]
    loggers: dict[str, LoggerConfig]
    root: dict[str, dict[str, list[str]]]

    @classmethod
    def from_dict(cls, config_dict: dict[str, Any]) -> LoggingConfig:
        return cls(**config_dict)


def load_logging_config(filepath: Path | str) -> LoggingConfig:
    config_dict = load_config(filepath, Config)
    logging_config = config_dict["log"]

    formatters = {
        k: FormatterConfig(**v) for k, v in logging_config["formatters"].items()
    }

    loggers = {k: LoggerConfig(**v) for k, v in logging_config["loggers"].items()}
    root = {k: dict(**v) for k, v in logging_config["root"].items()}

    return LoggingConfig(
        formatters=formatters, handlers=handlers, loggers=loggers, root=root
    )
