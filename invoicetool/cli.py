#!/usr/bin/env python
"""CLI tools for creating and working with an invoices database"""

from pathlib import Path

import click

from invoicetool import __version__
from invoicetool.config import Config
from invoicetool.hashes import calculate_hashes
from invoicetool.iotools import (
    build_output_directory,
    build_ymd_output_directory,
    copy_files,
    ensure_dir,
    get_filepaths_of_interest,
    get_word_documents,
    make_archive,
    pathify,
    remove_directory_with_files_matching_extensions,
    write_json,
)
from invoicetool.log import get_logger


@click.group()
@click.version_option(version=__version__)
def cli():
    """CLI tools for creating and working with an invoices database"""


base_output_directory_option = click.option(
    "-o",
    "--output-directory",
    "base_output_directory",
    type=click.Path(resolve_path=True, path_type=Path, file_okay=False),
)
start_dir_argument = click.argument(
    "start_dir", type=click.Path(resolve_path=True, path_type=Path, file_okay=False)
)
config_option = click.option(
    "-c",
    "--config",
    "config_filepath",
    type=click.Path(resolve_path=True, path_type=Path, dir_okay=False),
    help="path to config file",
)


@cli.command()
@base_output_directory_option
@start_dir_argument
@config_option
def export(
    start_dir: Path,
    base_output_directory: Path | None = None,
    config_filepath: Path | None = None,
):
    """Export Word documents to JSON format"""
    logger = get_logger()
    config = Config.from_file(config_filepath)
    logger.info(config)

    # the `~` doesn't get expanded with `click.Path`
    start_dir = pathify(start_dir)

    # TODO: tidy this up
    base_output_directory_ = (
        pathify(base_output_directory)
        if base_output_directory is not None
        else config.base_output_directory
    )
    output_directory_ = build_ymd_output_directory(base_output_directory_)
    ensure_dir(output_directory_)

    word_documents = [
        doc
        for doc in get_word_documents(
            start_dir,
            exclude_directories=config.exclude_directories,
        )
        if doc.hash not in config.exclude_hashes
    ]
    logger.info(f"→ {len(word_documents)} unique Word documents")
    write_json(
        [w.to_dict() for w in word_documents], output_directory_ / "word-documents.json"
    )


@cli.command()
@base_output_directory_option
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
    start_dir: Path,
    archive: bool,
    base_output_directory: Path | None = None,
    config_filepath: Path | None = None,
) -> None:
    """Search for & copy Word documents"""
    logger = get_logger()
    config = Config.from_file(config_filepath)
    logger.info(config)

    # the `~` doesn't get expanded with `click.Path`
    start_dir = pathify(start_dir)

    base_output_directory_ = (
        pathify(base_output_directory)
        if base_output_directory is not None
        else config.base_output_directory
    )
    # output_directory_ = base_output_directory / YYYY-MM-DD / START_DIR
    output_directory_ = build_output_directory(base_output_directory_, start_dir)

    document_filepaths = list(get_filepaths_of_interest(start_dir, config.extensions))
    num_documents = len(document_filepaths)
    logger.info(f"→ found {num_documents} documents of interest")
    logger.debug(f"→ documents: {document_filepaths}")

    copy_files(output_directory_, document_filepaths)

    if archive:
        # TODO: allow configuration of compression format via config file and command line option
        archive_path = make_archive(output_directory_)
        # we don't need the uncompressed directory anymore so remove it
        remove_directory_with_files_matching_extensions(
            output_directory_,
            extensions=config.extensions,
            dry_run=False,
            logger=logger,
        )
        logger.info(
            f"→ created compressed archive with {num_documents} documents at {archive_path}"
        )
    else:
        logger.info(f"→ copied {num_documents} documents to {output_directory_}")


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
#     default=8192,
#     type=int,
#     help="block size to read when computing the hash",
#     show_default=True,
# )
@base_output_directory_option
@start_dir_argument
@config_option
def hashes(
    start_dir: Path,
    base_output_directory: Path | None = None,
    config_filepath: Path | None = None,
    hash_function: str | None = None,
):
    """Compute the hashes of Word documents"""
    logger = get_logger()
    config = Config.from_file(config_filepath)
    logger.info(config)

    # the `~` doesn't get expanded with `click.Path`
    start_dir = pathify(start_dir)

    base_output_directory_ = (
        pathify(base_output_directory)
        if base_output_directory is not None
        else config.base_output_directory
    )
    output_directory_ = build_output_directory(base_output_directory_, start_dir)

    hash_algo = hash_function or config.hash_function_algorithm
    hashes = calculate_hashes(start_dir, config.extensions, hash_algo)
    duplicates = get_duplicate_files(hashes)
    write_json(hashes, output_directory_.parent / "hashes.json")
    write_json(duplicates, output_directory_.parent / "duplicates.json")
    logger.info(f"Wrote hashes and duplicates to {output_directory_.parent!s}")


if __name__ == "__main__":
    cli()
