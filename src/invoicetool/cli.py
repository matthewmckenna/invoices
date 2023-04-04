#!/usr/bin/env python
"""Find & extract all files of a given filetype from a directory"""
from __future__ import annotations

from pathlib import Path

import click

from . import __version__
from .config import get_working_directory, load_config
from .dates_times import today2ymd
from .iotools import copy_files, ensure_path, get_filepaths_of_interest, make_archive
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
) -> Path:
    """Dump all documents starting at START_DIR"""
    logger = setup_logging()
    config = load_config(config_filepath)
    logger.info(config)

    working_directory = output_directory if output_directory else get_working_directory()
    logger.info(f"Using working directory: {working_directory}")

    document_filepaths = list(get_filepaths_of_interest(start_dir, config.extensions))
    num_documents = len(document_filepaths)
    logger.info(f"Found {num_documents} documents of interest")
    logger.debug(f"Documents: {document_filepaths}")

    # construct the destination directory
    # destination = working_directory / YYYY-MM-DD / START_DIR
    destination = ensure_path(working_directory / today2ymd() / start_dir.stem)

    if archive:
        # TODO: allow configuration of compression format via
        # config file and command line option
        archive_path = make_archive(destination)
        logger.info(f"Created compressed archive {archive_path}")
    else:
        copy_files(destination, document_filepaths)
        logger.info(f"Copied {num_documents} documents to {destination}")

    return destination
