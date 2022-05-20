#!/usr/bin/env python
"""script to generate file hashes for files in a given directory"""
import argparse
# from collections import defaultdict
# from dataclass import dataclass
# from functools import partial
# import hashlib
import json
# import os
from pathlib import Path
# from typing import Iterator, Union

from get_duplicates import get_hash, scantree


# @dataclass
# class File:
#     file_hash: str
#     file_size: int
#     path: str


def main(args):
    """main entry point for the script"""
    directory = Path(args.directory)

    # file extensions we're interested in
    # TODO: use `args.extension`
    extensions = {'.doc', '.docx'}

    # dictionary to store file hashes
    # hashes = defaultdict(list)
    hashes = list()
    # we're only interested in unique hashes

    for entry in scantree(directory):
        # create a path object if we're dealing with a file
        p = Path(entry.path)

        # skip files with extensions we're not interested in
        if p.suffix not in extensions:
            continue

        # calculate the file hash
        file_hash = get_hash(p, args.algorithm)

        hashes.append(file_hash)

        # add the hash to the dict
        # files.append(File(file_hash, p.stat().st_size, p.as_posix()))

    hashes = list(set(hashes))
    # we only want entries with more than one value
    # duplicates = {k: v for k, v in hashes.items() if len(v) > 1}

    # order the dict by most duplicate files
    # ordered_duplicates = dict(sorted(
    #     duplicates.items(),
    #     key=lambda d: len(d[1]),
    #     reverse=True,
    # ))

    output_filepath = 'data/unique_hashes.json'

    with open(output_filepath, 'wt') as f:
        json.dump({'hashes': hashes}, f, indent=2)

    print(f'wrote unique hashes to {output_filepath}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='get hashes for files in a directory',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        '-a',
        '--algorithm',
        choices=['MD5', 'SHA1', 'SHA256', 'SHA512'],
        default='MD5',
        type=str.upper,
        help='hashing algorithm to use',
    )
    # parser.add_argument(
    #     '-e',
    #     '--extension',
    #     help='file extensions to look for',
    # )
    parser.add_argument('directory', help='starting directory')
    args = parser.parse_args()
    main(args)
