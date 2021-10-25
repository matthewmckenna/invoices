#!/usr/bin/env python
"""script to find null-ish files and remove them"""
import argparse
import os
from pathlib import Path
from typing import Iterator

from get_duplicates import scantree


def scan_dirs(path: Path) -> Iterator[os.DirEntry[str]]:
    """recursively yield directories starting from `path`"""
    for entry in os.scandir(path):
        if entry.is_dir():
            yield from scan_dirs(entry.path)
            yield entry
        else:
            continue


def remove_empty_directories(directory: Path, *, dry_run: bool = False):
    """recursively remove empty directories starting from `directory`"""
    for entry in scan_dirs(directory):
        # create a Path object
        p = Path(entry.path)

        # the directory is empty
        if not next(p.iterdir(), None):
            print(f'removing empty directory {p}... ', end='')
            if not dry_run:
                p.rmdir()
                print('done')


def remove_temporary_word_files(directory: Path, *, dry_run: bool = False):
    """recursively scan for and remove any temporary ms word files"""
    extensions = {'.doc', '.docx'}

    for entry in scantree(directory):
        # create a Path object
        p = Path(entry.path)

        # skip files with extensions we're not interested in
        if p.suffix not in extensions:
            continue

        # remove any temporary files
        if p.name.startswith('~$') and p.stat().st_size == 162:
            print(f'removing temp file {p}... ', end='')
            if not args.dry_run:
                p.unlink()
                print('done')


def main(args):
    """main entry point for the script"""
    directory = Path(args.directory)

    # find and remove any temporary ms word documents
    remove_temporary_word_files(directory, dry_run=args.dry_run)

    # find and remove any empty directories
    remove_empty_directories(directory, dry_run=args.dry_run)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='find and remove temporary ms word files',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        '-n',
        '--dry-run',
        action='store_true',
        help='perform a dry-run. does not delete any files or directories',
    )
    parser.add_argument('directory', help='starting directory to look for files')
    args = parser.parse_args()
    main(args)
