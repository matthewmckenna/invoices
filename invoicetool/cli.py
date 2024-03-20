#!/usr/bin/env python
"""CLI tools for creating and working with an invoices database"""

from __future__ import annotations

from pathlib import Path

import click

from . import __version__
from .config import get_working_directory, load_config
from .dates_times import today2ymd
from .hashes import calculate_hashes, get_duplicate_files, get_hash_function
from .iotools import (
    copy_files,
    ensure_path,
    get_filepaths_of_interest,
    make_archive,
    write_duplicates,
    write_hashes,
)
from .log import setup_logging


@click.group()
@click.version_option(version=__version__)
def cli():
    """CLI tools for creating and working with an invoices database"""
    pass


# @cli.command()
# @click.option(
#     "-d",
#     "--directory",
#     # default=lambda get_path():,
#     help="directory to remove",
#     type=click.Path(resolve_path=True, path_type=Path),
# )
# def delete_invoicedb(directory: Path):
#     """Delete all files in INVOICE_DB_DIR"""
#     directory = directory or get_path()
#     log.warn("Remove invoicedb directory", directory=directory)
#     # shutil.rmtree(directory)

start_dir_argument = click.argument(
    "start_dir", type=click.Path(resolve_path=True, path_type=Path, file_okay=False)
)
config_option = click.option(
    "-c",
    "--config",
    "config_filepath",
    type=click.Path(resolve_path=True, path_type=Path, dir_okay=False),
    help="path to config file",
    default="./config.toml",
    show_default=True,
)


@cli.command()
@click.option(
    "-o",
    "--output-directory",
    type=click.Path(resolve_path=True, path_type=Path, file_okay=False),
)
@click.option(
    "-a",
    "--archive",
    is_flag=True,
    default=False,
    help="create a compressed archive",
)
@start_dir_argument
@config_option
def dump_documents(
    start_dir: Path, output_directory: Path | None, config_filepath: Path, archive: bool
) -> Path:
    """Search for & copy Word documents"""
    logger = setup_logging()
    config = load_config(config_filepath)
    logger.info(config)

    working_directory = output_directory or get_working_directory()
    logger.info(f"Using working directory: {working_directory}")

    document_filepaths = list(get_filepaths_of_interest(start_dir, config.extensions))
    num_documents = len(document_filepaths)
    logger.info(f"Found {num_documents} documents of interest")
    logger.debug(f"Documents: {document_filepaths}")

    # construct the destination directory
    # destination = working_directory / YYYY-MM-DD / START_DIR
    destination = ensure_path(working_directory / today2ymd() / start_dir.stem)

    copy_files(destination, document_filepaths)
    logger.info(f"Copied {num_documents} documents to {destination}")

    if archive:
        # TODO: allow configuration of compression format via
        # config file and command line option
        archive_path = make_archive(destination)
        logger.info(f"Created compressed archive {archive_path}")

    return destination


@cli.command()
@click.option(
    "-a",
    "--algorithm",
    "hash_function",
    type=click.Choice(["MD5", "SHA1", "SHA256", "SHA512"], case_sensitive=False),
    help="algorithm to use for the hash function",
)
# @click.option(
#     "-b",
#     "--block-size",
#     default=4096,
#     type=int,
#     help="block size to read when computing the hash",
#     show_default=True,
# )
@start_dir_argument
@config_option
def hashes(start_dir: Path, config_filepath: Path, hash_function: str | None = None):
    """Compute the hashes of Word documents"""
    logger = setup_logging()
    config = load_config(config_filepath)
    logger.info(config)

    hash_algo = hash_function or get_hash_function(config.hash_function_algorithm)
    hashes = calculate_hashes(start_dir, config.extensions, hash_algo)
    duplicates = get_duplicate_files(hashes)
    write_hashes(hashes, directory=start_dir)
    write_duplicates(duplicates, directory=start_dir)
    logger.info(f"Wrote hashes and duplicates to {start_dir!s}")


if __name__ == "__main__":
    cli()
