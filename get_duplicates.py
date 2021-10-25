#!/usr/bin/env python
"""script to find a list duplicate files in a given directory"""
import argparse
from collections import defaultdict
from functools import partial
import hashlib
import json
import os
from pathlib import Path
from typing import Iterator, Union


def get_hash(
    filename: Union[str, Path],
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
        'MD5': hashlib.md5(),
        'SHA1': hashlib.sha1(),
        'SHA256': hashlib.sha256(),
        'SHA512': hashlib.sha512(),
    }
    hash_fn = hash_map[hash_function]

    with open(filename, 'rb') as f:
        for chunk in iter(partial(f.read, block_size), b''):
            hash_fn.update(chunk)

    return hash_fn.hexdigest()


def scantree(path: Path) -> Iterator[os.DirEntry[str]]:
    """recursively yield `DirEntry` objects for given directory"""
    for entry in os.scandir(path):
        if entry.is_dir():
            yield from scantree(entry.path)
        else:
            yield entry


def main(args):
    """main entry point for the script"""
    # directory = Path('data/invoice-docs')
    directory = Path(args.directory)

    # file extensions we're interested in
    # TODO: use `args.extension`
    extensions = {'.doc', '.docx'}

    # dictionary to store file hashes
    hashes = defaultdict(list)

    for entry in scantree(directory):
        if entry.is_file():
            # create a path object if we're dealing with a file
            p = Path(entry.path)

            # skip files with extensions we're not interested in
            if p.suffix not in extensions:
                continue

            # calculate the file hash
            file_hash = get_hash(p, args.algorithm)

            # add the hash to the dict
            hashes[file_hash].append(p.as_posix())

    # we only want entries with more than one value
    duplicates = {k: v for k, v in hashes.items() if len(v) > 1}

    # order the dict by most duplicate files
    ordered_duplicates = dict(sorted(
        duplicates.items(),
        key=lambda d: len(d[1]),
        reverse=True,
    ))

    output_filepath = 'data/duplicates.json'

    with open(output_filepath, 'wt') as f:
        json.dump(ordered_duplicates, f, indent=2)

    print(f'wrote duplicates list to {output_filepath}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='find duplicate files in a given directory',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        '-a',
        '--algorithm',
        choices=['MD5', 'SHA1', 'SHA256', 'SHA512'],
        default='MD5',
        type=str.upper,
        help='hashing algorithm to use'
    )
    # parser.add_argument(
    #     '-e',
    #     '--extension',
    #     help='file extensions to look for',
    # )
    parser.add_argument('directory', help='starting directory to look for duplicate files')
    args = parser.parse_args()
    main(args)
