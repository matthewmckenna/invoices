from __future__ import annotations

import hashlib
import json
import os
from collections import defaultdict
from functools import partial
from pathlib import Path
from typing import Iterator

import click

from .config import Config
from .dates_times import today2ymd
from .iotools import filepaths_with_extensions


@click.command()
@click.argument(
    "filename", type=click.Path(exists=True, dir_okay=False, resolve_path=True, path_type=Path)
)
@click.option(
    "-a",
    "--algorithm",
    "hash_function",
    type=click.Choice(["MD5", "SHA1", "SHA256", "SHA512"]),
    default="SHA1",
    help="algorithm to use for the hash function",
    case_sensitive=False,
)
@click.option(
    "-b", "--block-size", default=4096, type=int, help="Block size to read when computing the hash."
)
def calculate_hash(
    filename: Path | str,
    hash_function: str,
    *,
    block_size: int = 4096,
) -> str:
    """Return the hash for `filename`.

    Args:
        filename: name of the file of interest.
        hash_function: string name of hash function to use. valid
            choices are (`md5`, `sha1`, `sha256`, `sha512`).

    Keyword-only args:
        block_size: block size to read when computing the hash

    Returns:
        hexidecimal representation of secure hash (digest) for given
            hash function.
    """
    hash_map = {
        "MD5": hashlib.md5(),
        "SHA1": hashlib.sha1(),
        "SHA256": hashlib.sha256(),
        "SHA512": hashlib.sha512(),
    }

    # Raise a ValueError if an invalid hash function is passed in.
    if hash_function not in hash_map:
        raise ValueError(f"Invalid hash function: {hash_function}")

    hash_fn = hash_map[hash_function]

    with open(filename, "rb") as f:
        for chunk in iter(partial(f.read, block_size), b""):
            hash_fn.update(chunk)

    return hash_fn.hexdigest()


def main(directory: Path, config: Config) -> None:
    """main entry point for the script"""
    # dictionary to store file hashes
    hashes = defaultdict(list)

    for filepath in filepaths_with_extensions(directory, config.extensions):
        file_hash = calculate_hash(filepath, config.hash_function_algorithm)
        hashes[file_hash].append(filepath.as_posix())

    # we only want entries with more than one value
    duplicates = {k: v for k, v in hashes.items() if len(v) > 1}

    # sort the dict by most duplicate files
    sorted_duplicates = dict(
        sorted(
            duplicates.items(),
            key=lambda d: len(d[1]),
            reverse=True,
        )
    )

    if config.write_duplicates:
        write_duplicates_to_file(sorted_duplicates)


def write_duplicates_to_file(duplicates: dict[str, list[str]], config: Config) -> None:
    """Write the duplicates to a JSON file."""
    duplicates_filepath = config.working_directory / today2ymd() / "duplicates.json"
    write_json(duplicates, duplicates_filepath)
    with open(duplicates_filepath, "wt") as f:
        json.dump(sorted_duplicates, f, indent=2)

    print(f"wrote duplicates list to {output_filepath}")
