from pathlib import Path

import pytest

from invoicetool.config import Config


@pytest.fixture
def config(tmp_path_factory) -> Config:
    """Return a default config object"""
    working_dir = tmp_path_factory.mktemp("working_dir")
    return Config(
        extensions=[".doc", ".docx"], working_directory=working_dir, hash_function_algorithm="sha1"
    )


@pytest.fixture(scope="session")
def invoices_dir(tmp_path_factory):
    """Create a simple directory structure with different filetypes.

    Directory structure:
    .
    ├── another-level
    │   ├── document03.doc
    │   └── spreadsheet02.xlsx
    ├── document01.doc
    ├── document02.docx
    └── spreadsheet01.xls

    """
    invoices_dir = tmp_path_factory.mktemp("invoices")
    another_level = invoices_dir / "another-level"
    another_level.mkdir()

    for filepath in [
        invoices_dir / "document01.doc",
        invoices_dir / "document02.docx",
        invoices_dir / "spreadsheet01.xls",
        another_level / "document03.doc",
        another_level / "spreadsheet02.xlsx",
    ]:
        filepath.touch()

    return invoices_dir


@pytest.fixture(scope="function")
def empty_directory(tmp_path_factory: pytest.TempPathFactory) -> Path:
    empty_dir = tmp_path_factory.mktemp("empty_directory")
    return empty_dir


@pytest.fixture(scope="function")
def non_empty_directory(tmp_path: Path) -> Path:
    (tmp_path / "file.txt").touch()
    return tmp_path


@pytest.fixture(scope="function")
def nested_empty_directories(tmp_path_factory: pytest.TempPathFactory) -> Path:
    path = tmp_path_factory.mktemp("nested")
    (path / "empty1" / "empty2").mkdir(parents=True, exist_ok=True)
    return path
