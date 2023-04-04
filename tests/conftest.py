import pytest

from invoicetool.config import Config


@pytest.fixture
def config(tmp_path_factory) -> Config:
    """Return a default config object"""
    working_dir = tmp_path_factory.mktemp("working_dir")
    return Config(extensions=[".doc", ".docx"], working_directory=working_dir)
