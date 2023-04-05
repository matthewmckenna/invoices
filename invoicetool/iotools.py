from __future__ import annotations

import json
import logging
import os
import shutil
from pathlib import Path
from typing import Any, Iterable, Iterator


def ensure_path(path: Path | str):
    """Ensure that a directory exists, creating if needed"""
    if isinstance(path, str):
        path = Path(path)

    if "." in path.name:
        path = path.parent

    pathify(path).mkdir(exist_ok=True, parents=True)
    return path


def scantree(path: Path) -> Iterator[os.DirEntry[str]]:
    """Recursively yield `DirEntry` objects for given directory"""
    for entry in os.scandir(path):
        if entry.is_dir():
            yield from scantree(entry.path)
        else:
            yield entry


def filepaths_with_extensions(directory: Path, extensions: Iterable[str]):
    """Yield a sequence of absolute filepaths starting from the
    `directory` which match `extensions`.
    """
    for entry in scantree(directory):
        p = Path(entry.path)

        # skip files with extensions not in `extensions`
        if p.suffix not in extensions:
            continue

        yield pathify(p)


def get_filepaths_of_interest(target: Path, extensions: Iterable[str]) -> Iterator[Path]:
    """Yield a sequence of absolute filepaths starting from the
    `target` directory which match `extensions`.
    """
    for filepath in filepaths_with_extensions(target, extensions):
        if is_empty_file(filepath):
            continue
        yield filepath


def remove_temporary_word_files(directory: Path, *, dry_run: bool = False, logger: logging.Logger):
    """recursively scan for and remove any temporary ms word files"""
    # Hard-code the extensions as we're removing specific file types
    extensions = {".doc", ".docx"}

    for filepath in filepaths_with_extensions(directory, extensions):
        if is_empty_file(filepath):
            logger.info(f"Remove temporary Word document: {filepath.name}")
            filepath.unlink()


def is_empty_file(path: Path) -> bool:
    """Return whether or not a file is an empty temporary MS Word document.

    Checks:
    - If the filename begins with `~$`
    - If the file size is exactly 162 bytes

    Files which match these criteria are empty temporary MS Word documents.
    """
    return path.name.startswith("~$") and path.stat().st_size == 162


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
        dst = destination / get_relative_filepath(src, destination.stem)

        # create the files parent directory if it doesn't exist
        _ = ensure_path(dst)

        # copy the file from `src` to `dst`
        shutil.copy2(src, dst)


def get_relative_filepath(abs_filepath: Path, start_dir: Path) -> Path:
    """Get the filepath relative to start_dir"""
    return Path(str(abs_filepath).rsplit(start_dir, maxsplit=1)[-1].lstrip("/"))


def make_archive(destination: Path, *, format: str = "bztar") -> Path:
    """Create an archive named `destination`.`format`

    Defaults to creating a `.tar.bz2` archive.

    format:
      - zip
      - tar
      - gztar
      - bztar
      - xztar
    """
    archive_path = shutil.make_archive(
        base_name=destination,
        format=format,
        root_dir=destination.parent,
    )
    return Path(archive_path)


def write_json(obj: Any, filepath: Path) -> None:
    """Write an object to a JSON file."""
    if isinstance(filepath, str):
        filepath = pathify(filepath)
    filepath.write_text(json.dumps(obj, indent=2))


def load_json(obj: Any, filepath: Path) -> dict[str, Any]:
    """Load a JSON file into a dictionary."""
    if isinstance(filepath, str):
        filepath = pathify(filepath)
    return json.loads(filepath.read_text())


def pathify(path: Path | str) -> Path:
    """Return an absolute Path object with the home directory expanded"""
    if isinstance(path, str):
        path = Path(path)
    return path.expanduser().resolve()


def write_hashes(hashes: dict[str, list[str]], directory: Path):
    hashes_filepath = directory.parent / "hashes.json"
    write_json(hashes, hashes_filepath)


def write_duplicates(duplicates: dict[str, list[str]], directory: Path):
    # duplicates = get_duplicate_files(hashes)
    duplicates_filepath = directory.parent / "duplicates.json"
    write_json(duplicates, duplicates_filepath)


# def write_duplicates_to_file(duplicates: dict[str, list[str]], config: Config) -> None:
#     """Write the duplicates to a JSON file."""
#     duplicates_filepath = config.working_directory / today2ymd() / "duplicates.json"
#     write_json(duplicates, duplicates_filepath)


def yield_dirs(path: Path) -> Iterator[Path]:
    """Recursively yield directories starting from `path`"""
    for entry in path.iterdir():
        if entry.is_dir():
            yield from yield_dirs(entry)
            yield entry
        else:
            continue


def remove_empty_directories(directory: Path) -> None:
    """Recursively remove empty directories starting from `directory`"""
    for subdirectory in yield_dirs(directory):
        remove_directory_if_empty(subdirectory)
    remove_directory_if_empty(directory)


def directory_is_empty(directory: Path) -> bool:
    """Return whether or not a directory is empty"""
    return not next(directory.iterdir(), None)


def remove_directory_if_empty(directory: Path) -> None:
    """Remove the working directory if it's empty"""
    if directory_is_empty(directory):
        directory.rmdir()
