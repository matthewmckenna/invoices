#!/usr/bin/env python
"""Find & extract all files of a given filetype from a directory"""
import os
from pathlib import Path
import shutil
import sys
from typing import Iterable, Iterator, List, Set

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


def get_filepaths_of_interest(target: str, extensions: Set[str]) -> Iterator[Path]:
    """Yield a sequence of absolute filepaths starting from the
    `target` directory which match `extensions`.
    """
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
        # Start by getting a list of all the files to be copied
        yield p.expanduser()


def copy_files(destination: Path, filepaths: Iterable[Path]) -> None:
    """
    Copy files in `filepaths` from `src` to `dst`.

    `destination` is the parent directory where the original
    directory structure will be mirrored to.
    """
    for filepath in filepaths:
        # path to the original file
        src = filepath

        # path to the new destination file
        # we want to skip the first three elements of the source filepath:
        # `('/', 'Users', 'username')`
        dst = destination / Path(*filepath.parts[3:])

        # create the files parent directory if it doesn't exist
        dst.parent.mkdir(parents=True, exist_ok=True)

        # copy the file from `src` to `dst`
        shutil.copy2(src, dst)


def make_archive(destination: Path, *, format="gztar") -> None:
    """Create an archive named `destination`.`format``

    Defaults to creating a `.gzip` archive.
    """
    # TODO: check if I need the base_name & root_dir
    archive_path = shutil.make_archive(
        base_name=destination,
        format=format,
        root_dir=destination,
    )
    # TODO: log this rather than print
    print(f"created archive: {archive_path}")


@click.command()
@click.argument("--extensions", "-e", required=True)
# @click.argument("--target", "-t", required=True)
# @click.argument("--destination", "-d")
# @click.option("--archive", "-a", default=False, is_flag=True)
# def main(extensions: List[str], target: str, destination: str, archive: bool):
def main():
    """Find and extract all files of a given filetype"""
    # TODO: can I denote the click argument as a set?
    return
    extensions = set(extensions)

    # Get a list of filepaths of interest
    # TODO: may need to cast this to a list to get the length
    filepaths = get_filepaths_of_interest(target, extensions)

    copy_files(destination, filepaths)
    # TODO: add this as logging
    print(f"copied {len(filepaths)} documents to {destination}")

    # Find all files matching extensions
    if archive:
        make_archive(destination)


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
