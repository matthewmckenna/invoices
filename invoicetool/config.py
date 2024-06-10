import tomllib
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import ClassVar

from invoicetool.iotools import FileFormat, ensure_dir, pathify


@dataclass
class Config:
    _DEFAULT_EXTENSION_ALLOW_LIST: ClassVar[set[str]] = FileFormat.word_docs_default_extensions()
    _DEFAULT_CONFIG_PATH: ClassVar[str] = "./config.toml"
    _DEFAULT_BASE_OUTPUT_DIRECTORY: ClassVar[str] = "~/.invoicetool"
    _DEFAULT_HASH_FUNCTION_ALGORITHM: ClassVar[str] = "sha1"
    _DEFAULT_CUSTOMER_MAP_PATH: ClassVar[str] = (
        f"{_DEFAULT_BASE_OUTPUT_DIRECTORY}/config/customer-map.json"
    )

    hash_function_algorithm: str
    base_output_directory: Path
    # TODO: I'm not really happy with this, but it's OK for now
    customer_map_path: Path | None = None
    extensions: set[str] = field(default_factory=set)
    exclude_directories: set[str] = field(default_factory=set)
    include_directories: set[str] = field(default_factory=set)
    exclude_file_hashes: set[str] = field(default_factory=set)

    def __post_init__(self):
        if self.customer_map_path is not None:
            self.customer_map_path = pathify(self.customer_map_path)
        self.base_output_directory = pathify(self.base_output_directory)
        self.extensions = set(self.extensions)
        self.exclude_directories = set(self.exclude_directories)
        self.include_directories = set(self.include_directories)
        self.exclude_file_hashes = set(self.exclude_file_hashes)
        ensure_dir(self.base_output_directory)

    def __str__(self):
        return f"Config(base_output_directory={self.base_output_directory}, extensions={self.extensions}, hash_function={self.hash_function_algorithm})"

    @classmethod
    def from_dict(cls, d) -> "Config":
        return cls(**d)

    def to_dict(self):
        return asdict(self)

    @classmethod
    def default(cls) -> "Config":
        return cls(
            extensions=cls._DEFAULT_EXTENSION_ALLOW_LIST,
            base_output_directory=cls._DEFAULT_BASE_OUTPUT_DIRECTORY,
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
