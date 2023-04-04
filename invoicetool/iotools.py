import os
import shutil
from pathlib import Path
from typing import Iterable, Iterator


def ensure_path(path: Path | str):
    """Ensure that a directory exists, creating if needed"""
    if isinstance(path, str):
        path = Path(path)

    if "." in path.name:
        path = path.parent

    path.expanduser().mkdir(exist_ok=True, parents=True)
    return path


def scantree(path: Path) -> Iterator[os.DirEntry[str]]:
    """Recursively yield `DirEntry` objects for given directory"""
    for entry in os.scandir(path):
        if entry.is_dir():
            yield from scantree(entry.path)
        else:
            yield entry


def get_filepaths_of_interest(target: Path, extensions: Iterable[str]) -> Iterator[Path]:
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

        yield p.expanduser().resolve()


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
