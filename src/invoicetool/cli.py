#!/usr/bin/env python
"""Find & extract all files of a given filetype from a directory"""
from __future__ import annotations

import os
import shutil
import sys
from pathlib import Path
from typing import Iterable, Iterator

import click

from . import __version__
from .config import get_working_directory, load_config
from .dates_times import today2ymd
from .iotools import ensure_path
from .log import setup_logging


@click.group()
# @click.argument("--extensions", "-e", required=True)
@click.version_option(version=__version__)
# @click.argument("--target", "-t", required=True)
# @click.argument("--destination", "-d")
# @click.option("--archive", "-a", default=False, is_flag=True)
# def main(extensions: List[str], target: str, destination: str, archive: bool):
def cli():
    """Utilities for creating and working with an invoices database"""
    pass


@cli.command()
def logr():
    """Log a message"""
    logger = setup_logging()
    logger.info("Hello, World!")


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


def get_filepaths_of_interest(target: Path, extensions: set[str]) -> Iterator[Path]:
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
        # dst = ORIGINAL_DESTINATION / START_DIR / RELATIVE_FILEPATH
        dst = destination / get_relative_filepath(src, destination.stem)
        # log.debug("Mirroring...", src=src, dst=dst)

        # create the files parent directory if it doesn't exist
        dst.parent.mkdir(parents=True, exist_ok=True)

        # copy the file from `src` to `dst`
        shutil.copy2(src, dst)


def get_relative_filepath(abs_filepath: Path, start_dir: Path) -> Path:
    """Get the filepath relative to start_dir"""
    return Path(str(abs_filepath).rsplit(start_dir, maxsplit=1)[-1].lstrip("/"))


def make_archive(destination: Path, *, format: str = "bztar") -> Path:
    """Create an archive named `destination`.`format`

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
        root_dir=destination.parent,
    )
    log.info("Created archive", archive_path=archive_path)
    return Path(archive_path)


@cli.command()
@click.option(
    "-d",
    "--directory",
    # default=lambda get_path():,
    help="directory to remove",
    type=click.Path(resolve_path=True, path_type=Path),
)
def delete_invoicedb(directory: Path):
    """Delete all files in INVOICE_DB_DIR"""
    directory = directory or get_path()
    log.warn("Remove invoicedb directory", directory=directory)
    # shutil.rmtree(directory)


@cli.command()
@click.argument("start_dir", type=click.Path(resolve_path=True, path_type=Path, file_okay=False))
@click.option(
    "-o", "--output-directory", type=click.Path(resolve_path=True, path_type=Path, file_okay=False)
)
@click.option(
    "-c",
    "--config",
    "config_filepath",
    type=click.Path(resolve_path=True, path_type=Path, dir_okay=False),
    help="path to config file",
    default="./config.toml",
)
@click.option(
    "-a",
    "--archive",
    is_flag=True,
    default=False,
    help="create a compressed archive",
)
def dump_documents(
    start_dir: Path, output_directory: Path | None, config_filepath: Path, archive: bool
):
    """Create a dump of all documents starting at START_DIR."""
    logger = setup_logging()
    config = load_config(config_filepath)
    logger.info(config)

    # get the date in the form YYYY-MM-DD
    # today = today2ymd()

    working_directory = output_directory if output_directory else get_working_directory()
    logger.info(f"Using working directory: {working_directory}")

    # ensure_path(destination / start_dir.stem)

    # list of absolute filepaths
    document_filepaths = list(get_filepaths_of_interest(start_dir, config.extensions))
    num_documents = len(document_filepaths)
    logger.info(f"Found {num_documents} documents")

    sys.exit(4)
    copy_files(destination, document_filepaths)
    logger.info(f"Copied {num_documents} documents to {destination}")

    # find all files matching extensions
    if archive:
        # should we pass in a compression format here?
        # does it need to be configurable?
        make_archive(destination)

    return destination
