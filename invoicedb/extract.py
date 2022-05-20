#!/usr/bin/env python
"""Find & extract all files of a given filetype from a directory"""
import os
from pathlib import Path
import sys
from typing import Iterator, List

import click


def yield_filepaths(filepath: str) -> Iterator[Path]:
    """yield Path objects from a manifest file `filepath`"""
    with open(filepath, "rt") as f:
        for line in f:
            yield Path(line.strip()).expanduser()


def scantree(path: Path) -> Iterator[os.DirEntry[str]]:
    """recursively yield `DirEntry` objects for given directory"""
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
    """Return whether or not a file is an empty temporary MS Word document

    Checks:
    - If the filename begins with `~$`
    - If the file size is exactly 162 bytes

    Files which match this criteria are empty temporary MS Word documents.
    """
    return path.name.startswith("~$") and path.stat().st_size == 162


@click.command
@click.argument("--extensions", "-e", required=True)
@click.argument("--target", "-t", required=True)
@click.argument("--destination", "-d")
def main(extensions: List[str], target: str, destination: str):
    """Find and extract all files of a given filetype"""
    # TODO: can I denote the click argument as a set?
    extensions = set(extensions)
    # Find all files matching extensions
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


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
