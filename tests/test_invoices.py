import tarfile
from pathlib import Path

import pytest
from click.testing import CliRunner
from invoicedb import __version__
from invoicedb.cli import cli


def test_version():
    assert __version__ == "0.1.0"


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


def test_document_dump(invoices_dir, tmp_path):
    runner = CliRunner()
    destination = tmp_path
    # in the main application code we strip off the first three elements
    # of the filepath ("/", "Users", "USERNAME")
    # docs_dir = destination / Path(*invoices_dir.parts[3:])
    # docs_dir = destination / str(invoices_dir).rsplit(destination.stem, maxsplit=1)[-1].lstrip("/")
    result = runner.invoke(
        cli,
        [
            "dump-documents",
            "--destination",
            destination,
            str(invoices_dir),
        ],
    )
    assert result.exit_code == 0
    # check if one of the documents created above exists
    assert (destination / invoices_dir.stem / "document02.docx").exists()


def test_document_dump_with_archive(invoices_dir, tmp_path, capsys):
    runner = CliRunner()
    destination = tmp_path
    expected_archive_filepath = Path(f"{destination / invoices_dir.stem}.tar.bz2")

    result = runner.invoke(
        cli,
        [
            "dump-documents",
            "--archive",
            "--destination",
            destination,
            str(invoices_dir),
        ],
    )

    with tarfile.open(expected_archive_filepath, "r") as tf:
        tf.list(verbose=False)
    output = capsys.readouterr().out.rstrip()

    dumped_document_filepaths = [p for p in output.splitlines() if Path(p.rstrip()).suffix]

    assert result.exit_code == 0
    assert expected_archive_filepath.exists()
    assert len(dumped_document_filepaths) == 3
