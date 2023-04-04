import pytest

from invoicetool.config import Config


@pytest.fixture
def config(tmp_path_factory) -> Config:
    """Return a default config object"""
    working_dir = tmp_path_factory.mktemp("working_dir")
    return Config(extensions=[".doc", ".docx"], working_directory=working_dir)


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
