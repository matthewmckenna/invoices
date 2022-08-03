#!/usr/bin/env python
"""Find & extract all files of a given filetype from a directory"""
import datetime
import os
from pathlib import Path
import shutil
import sys
from typing import Iterable, Iterator, Set

import click
import structlog

from . import __version__


log = structlog.get_logger()


@click.group()
# @click.argument("--extensions", "-e", required=True)
@click.version_option(version=__version__)
# @click.argument("--target", "-t", required=True)
# @click.argument("--destination", "-d")
# @click.option("--archive", "-a", default=False, is_flag=True)
# def main(extensions: List[str], target: str, destination: str, archive: bool):
def main():
    """Find and extract all files of a given filetype"""
    pass


def yield_filepaths(filepath: str) -> Iterator[Path]:
    """yield Path objects from a manifest file `filepath`"""
    with open(filepath, "rt") as f:
        for line in f:
            yield Path(line.strip()).expanduser()


def scantree(path: Path) -> Iterator[os.DirEntry[str]]:
    """Recursively yield `DirEntry` objects for given directory"""
    for entry in os.scandir(path):
        if entry.is_dir():
            yield from scantree(entry.path)
        else:
            yield entry


def remove_temporary_word_files(directory: Path, *, dry_run: bool = False):
    """recursively scan for and remove any temporary ms word files"""
    # Hard-code the extensions as we're removing specific file types
    extensions = {".doc", ".docx"}
    dry_run_message = "" if not dry_run else "DRY RUN: "

    for entry in scantree(directory):
        p = Path(entry.path)

        # skip files with extensions we're not interested in
        if p.suffix not in extensions:
            continue

        # remove any temporary files
        if is_empty_file(p):
            print(f"{dry_run_message}Removing temp file {p}")
            if not dry_run:
                p.unlink()


def is_empty_file(path: Path) -> bool:
    """Return whether or not a file is an empty temporary MS Word document.

    Checks:
    - If the filename begins with `~$`
    - If the file size is exactly 162 bytes

    Files which match these criteria are empty temporary MS Word documents.
    """
    return path.name.startswith("~$") and path.stat().st_size == 162


def get_filepaths_of_interest(target: Path, extensions: Set[str]) -> Iterator[Path]:
    """Yield a sequence of absolute filepaths starting from the
    `target` directory which match `extensions`.

    extensions: {".doc", ".docx"}
    """
    for entry in scantree(target):
        p = Path(entry.path)

        # Skip files with extensions not in `extensions`
        if p.suffix not in extensions:
            continue

        # Skip empty files
        # TODO: refactor this. maybe more checks to test if a file is empty
        if is_empty_file(p):
            continue

        # Copy the file
        # Should we copy files as we go, or build a list & copy at the end?
        # Start by getting a list of all the files to be copied
        yield p.expanduser()


def copy_files(destination: Path, filepaths: Iterable[Path]) -> None:
    """
    Copy files in `filepaths` from `src` to `dst`.

    `destination` is the parent directory where the original
    directory structure will be mirrored to.
    """
    for filepath in filepaths:
        # path to the original file
        src = filepath

        # path to the new destination file
        # we want to skip the first three elements of the source filepath:
        # `('/', 'Users', 'username')`
        dst = destination / Path(*filepath.parts[3:])
        # log.debug("Mirroring...", src=src, dst=dst)

        # create the files parent directory if it doesn't exist
        dst.parent.mkdir(parents=True, exist_ok=True)

        # copy the file from `src` to `dst`
        shutil.copy2(src, dst)


def make_archive(destination: Path, *, format: str = "bztar") -> Path:
    """Create an archive named `destination`.`format``

    Defaults to creating a `.tar.bz2` archive.

    format:
      - zip
      - tar
      - gztar
      - bztar
      - xztar
    """
    archive_path = shutil.make_archive(
        base_name=destination,
        format=format,
        root_dir=destination,
    )
    log.info("Created archive", archive_path=archive_path)
    return archive_path


@main.command()
@click.argument("filepath", type=click.Path(resolve_path=True))
@click.option(
    "-a",
    "--archive",
    is_flag=True,
    default=False,
    help="create a compressed archive"
)
def dump_documents(filepath: Path, archive: bool = False):
    """Create a dump of all documents starting at FILEPATH."""
    # TODO: add these to a config file
    extensions = {".doc", ".docx"}

    # get the date in the form YYYY-MM-DD
    today = datetime.date.today().isoformat()

    # should this be configurable?
    destination = get_path() / today
    destination.mkdir(exist_ok=True, parents=True)

    # list of absolute filepaths
    document_filepaths = list(get_filepaths_of_interest(filepath, extensions))
    num_documents = len(document_filepaths)
    log.info("Got document filepaths", num_documents=num_documents)

    # TODO: write out the filepaths as a manifest creation / debug step
    copy_files(destination, document_filepaths)
    log.info("Copied documents", num_documents=num_documents, destination=destination)

    # Find all files matching extensions
    if archive:
        # should we pass in a compression format here?
        # does it need to be configurable?
        make_archive(destination)


def get_path():
    """Get the path of the `invoicedb` data directory"""
    # TODO: document the use of environment variables here
    invoice_db_path_env = os.getenv("INVOICE_DB_DIR", "")

    if invoice_db_path_env:
        invoice_db_path = Path(invoice_db_path_env)
    else:
        invoice_db_path = Path.home() / "invoicedb"

    return invoice_db_path


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
