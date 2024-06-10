import hashlib
from collections import defaultdict
from functools import partial
from pathlib import Path


def calculate_hashes(
    paths: list[Path],
    hash_function: str,
) -> dict[str, list[str]]:
    """Calculate the hashes of all files in a directory"""
    hashes = defaultdict(list)
    for path in paths:
        file_hash = calculate_hash(path, hash_function)
        hashes[file_hash].append(path.as_posix())
    return hashes


def calculate_hash(
    filename: Path | str,
    *,
    hash_function: str = "sha1",
    block_size: int = 8192,
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
        "md5": hashlib.md5(),
        "sha1": hashlib.sha1(),
        "sha256": hashlib.sha256(),
        "sha512": hashlib.sha512(),
    }

    # Raise a ValueError if an invalid hash function is passed in.
    if hash_function not in hash_map:
        raise ValueError(f"Invalid hash function: {hash_function}")

    hash_fn = hash_map[hash_function]

    with open(filename, "rb") as f:
        for chunk in iter(partial(f.read, block_size), b""):
            hash_fn.update(chunk)

    return hash_fn.hexdigest()
