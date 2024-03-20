from __future__ import annotations

import hashlib
from collections import defaultdict
from functools import partial
from pathlib import Path

from .iotools import filepaths_with_extensions


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
    hash_function = hash_function.upper()
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


def get_duplicate_files(
    hashes: dict[str, list[str]], *, sort: bool = True
) -> dict[str, list[str]]:
    """Return a dictionary of files with duplicate hashes.

    Args:
        hashes: dictionary of hashes and the files that have that
            hash.

    Returns:
        dictionary of duplicate files, keyed by the hash.
    """
    duplicates = {k: v for k, v in hashes.items() if len(v) > 1}

    if sort:
        return dict(sorted(duplicates.items(), key=lambda d: len(d[1]), reverse=True))
    else:
        return duplicates


def get_hash_function(config_hash_function: str | None = None) -> str:
    """Get the hash function for `invoicetool`.

    In order of precedence:
      - `hash_function_algorithm` in `config.toml`
      - `sha1`
    """
    if config_hash_function:
        hash_function = config_hash_function
    else:
        hash_function = "sha1"

    return hash_function


def calculate_hashes(
    directory: Path, extensions: list[str], hash_function: str
) -> dict[str, list[str]]:
    """Calculate the hashes of all files in a directory"""
    hashes = defaultdict(list)
    for filepath in filepaths_with_extensions(directory, extensions):
        file_hash = calculate_hash(filepath, hash_function)
        hashes[file_hash].append(filepath.as_posix())
    return hashes
