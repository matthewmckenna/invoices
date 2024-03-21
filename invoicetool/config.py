from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import ClassVar

import tomllib

from invoicetool.iotools import ensure_dir, pathify


@dataclass
class Config:
    _DEFAULT_EXTENSION_ALLOW_LIST: ClassVar[set[str]] = {".doc", ".docx"}
    _DEFAULT_CONFIG_PATH: ClassVar[str] = "./config.toml"
    _DEFAULT_OUTPUT_DIRECTORY: ClassVar[str] = "~/.invoicetool"
    _DEFAULT_HASH_FUNCTION_ALGORITHM: ClassVar[str] = "sha1"

    hash_function_algorithm: str
    output_directory: Path
    extensions: set[str] = field(default_factory=set)

    def __post_init__(self):
        self.output_directory = pathify(self.output_directory)
        ensure_dir(self.output_directory)

    def __str__(self):
        return f"Config(output_directory={self.output_directory}, extensions={self.extensions}, hash_function={self.hash_function_algorithm})"

    @classmethod
    def from_dict(cls, d) -> "Config":
        return cls(**d)

    def to_dict(self):
        return asdict(self)

    @classmethod
    def default(cls) -> "Config":
        return cls(
            extensions=cls._DEFAULT_EXTENSION_ALLOW_LIST,
            output_directory=cls._DEFAULT_OUTPUT_DIRECTORY,
            hash_function_algorithm=cls._DEFAULT_HASH_FUNCTION_ALGORITHM,
        )

    @property
    def project_directory(self) -> Path:
        """Return the project directory path.

        The project directory is used to find the `config.toml`
        file, and to create the `logs` directory.

        The directory tree for this file is as follows:

        invoicetool_project  # project directory / repository
        └── invoicetool
            └── config.py

        Path(__file__) == Path("config.py")
        Path(__file__).parent == Path("invoicetool")
        Path(__file__).parent.parent == Path("invoicetool_project")
        """
        return Path(__file__).parent.parent

    @property
    def default_config_filepath(self) -> Path:
        """Return the default config filepath"""
        return self.project_directory / self._DEFAULT_CONFIG_PATH

    @classmethod
    def from_file(cls, path: str | None = None) -> "Config":
        path = cls._DEFAULT_CONFIG_PATH if path is None else path
        with open(path, "rb") as f:
            config_dict = tomllib.load(f)["invoicetool"]
        return cls.from_dict(config_dict)


# def get_working_directory(config: Config | None = None) -> Path:
#     """Get the working directory for `invoicetool`.

#     In order of precedence:
#       - `INVOICETOOL_WORKING_DIR` environment variable
#       - `working_directory` in `config.toml`
#       - `~/.invoicetool`
#     """
#     env_working_dir = os.getenv("INVOICETOOL_WORKING_DIR")
#     if env_working_dir:
#         working_directory = Path(env_working_dir)
#     elif config and config.working_directory:
#         working_directory = Path(config.working_directory)
#     else:
#         working_directory = Path.home() / ".invoicetool"

#     return working_directory.expanduser().resolve()
