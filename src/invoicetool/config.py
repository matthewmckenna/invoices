from __future__ import annotations

import json
import tomllib
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass
class Config:
    extensions: list[int]
    working_path: Path

    def __post_init__(self):
        self.working_path = Path(self.working_path).expanduser()


def get_project_directory() -> Path:
    """Return the project directory path.

    The project directory is used to find the `config.toml`
    file, and to create the `logs` directory.

    The directory tree for this file is as follows:

    invoicetool_project  # project directory / repository
    └── src
        └── invoicetool
            └──  config.py

    Path(__file__) == Path("config.py")
    Path(__file__).parent == Path("invoicetool")
    Path(__file__).parent.parent == Path("src")
    Path(__file__).parent.parent.parent == Path("invoicetool_project")
    """
    return Path(__file__).parent.parent.parent


def get_default_config_filepath() -> Path:
    """Return the default config filepath"""
    project_directory = get_project_directory()
    return project_directory / "config.toml"


def load_config(filepath: Path | str) -> Config:
    """Load a config file and return as a Config object"""
    config_dict = load_config_dict(filepath)
    return Config(**config_dict["invoicetool"])


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
