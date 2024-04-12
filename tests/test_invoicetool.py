import tarfile
from pathlib import Path

from click.testing import CliRunner

from invoicetool import __version__
from invoicetool.cli import cli
from invoicetool.dates_times import today2ymd


def test_version():
    assert __version__ == "0.1.0"


def test_document_dump(invoices_dir, tmp_path):
    runner = CliRunner()

    result = runner.invoke(
        cli,
        [
            "dump-documents",
            "--output-directory",
            tmp_path,
            str(invoices_dir),
        ],
    )
    assert result.exit_code == 0
    # check if one of the documents created above exists
    assert (tmp_path / today2ymd() / invoices_dir.name / "document02.docx").exists()


def test_document_dump_with_archive(invoices_dir, tmp_path, capsys):
    runner = CliRunner()
    destination = tmp_path / today2ymd() / invoices_dir.name
    expected_archive_filepath = Path(f"{destination}.tar.bz2")

    result = runner.invoke(
        cli,
        [
            "dump-documents",
            "--archive",
            "--output-directory",
            tmp_path,
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
