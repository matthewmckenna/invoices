import json
import logging
import shutil
from dataclasses import asdict, dataclass
from enum import StrEnum, auto
from pathlib import Path
from typing import Any, Iterable, Iterator

from invoicetool.dates_times import today2ymd
from invoicetool.hashes import calculate_hash


class FileFormat(StrEnum):
    DOC: str = auto()
    DOCX: str = auto()

    @classmethod
    def from_str(cls, s: str) -> "FileFormat":
        filetype_ = s.strip().lower()
        for supported_filetype in cls.__members__.values():
            if filetype_ == supported_filetype.value:
                return supported_filetype
        supported_filetypes = list(cls.__members__.keys())
        raise ValueError(
            f"unknown file type: {filetype_} (supported file types: {supported_filetypes})"
        )


@dataclass
class File:
    name: str
    original_path: str
    md5: str
    sha1: str
    modification_time: float | int
    size: int

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, d):
        return cls(**d)


def get_files_of_interest(
    path: Path,
    *,
    extensions: set[str] | None = None,
    filter_empty_files: bool = False,
    exclude_directories: set[str] | None = None,
) -> Iterator[Path]:
    for entry in path.iterdir():
        # TODO: this may not be right
        original_path = Path(*entry.parts[5:])
        if exclude_directories and any(
            original_path.match(exclude_directory)
            for exclude_directory in exclude_directories
        ):
            continue
        if entry.is_dir():
            yield from get_files_of_interest(
                entry,
                extensions=extensions,
                filter_empty_files=filter_empty_files,
                exclude_directories=exclude_directories,
            )
        elif extensions is None or entry.suffix in extensions:
            if not filter_empty_files or not is_empty_file(entry):
                stat_info = entry.stat()
                yield File(
                    name=entry.name,
                    original_path=original_path.as_posix(),
                    md5=calculate_hash(entry, "md5"),
                    sha1=calculate_hash(entry, "sha1"),
                    modification_time=stat_info.st_mtime,
                    size=stat_info.st_size,
                )


# def ensure_path(path: Path | str):
#     """Ensure that a directory exists, creating if needed"""
#     if isinstance(path, str):
#         path = Path(path)
#     if "." in path.name:
#         path = path.parent
#     ensure_dir(path)
#     return path


def ensure_dir(path: Path | str) -> None:
    """Ensure that a directory exists, creating if needed"""
    pathify(path).mkdir(exist_ok=True, parents=True)


def scantree(path: Path) -> Iterator[Path]:
    """Recursively yield `Path` objects for given directory"""
    for entry in path.iterdir():
        if entry.is_dir():
            yield from scantree(entry)
        else:
            yield entry


def filepaths_with_extensions(directory: Path, extensions: set[str]) -> Iterable[Path]:
    """Yield a sequence of absolute filepaths starting from `directory` which match `extensions`."""
    for filepath in scantree(directory):
        # skip files with extensions not in `extensions`
        if filepath.suffix not in extensions:
            continue
        yield pathify(filepath)


def get_filepaths_of_interest(directory: Path, extensions: set[str]) -> Iterator[Path]:
    """Yield a sequence of absolute filepaths starting from the
    `target` directory which match `extensions`.
    """
    for filepath in filepaths_with_extensions(directory, extensions):
        if is_empty_file(filepath):
            continue
        yield filepath


def remove_temporary_word_files(
    directory: Path, *, dry_run: bool = False, logger: logging.Logger
):
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
    # make sure the destination directory exists
    ensure_dir(destination)
    for filepath in filepaths:
        # path to the original file
        src = filepath

        # path to the new destination file
        dst = destination / get_relative_filepath(src, destination.name)

        # create the parent directory if it doesn't exist
        ensure_dir(dst.parent)

        # copy the file from `src` to `dst`
        shutil.copy2(src, dst)


def get_relative_filepath(abs_filepath: Path, start_dir: str) -> Path:
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
        base_name=str(destination),
        format=format,
        root_dir=destination.parent,
    )
    return Path(archive_path)


def write_json(obj: Any, filepath: Path) -> None:
    """Write an object to a JSON file."""
    filepath = pathify(filepath)
    filepath.write_text(json.dumps(obj, indent=2))


def pathify(path: Path | str) -> Path:
    """Return an absolute Path object with the home directory expanded"""
    if isinstance(path, str):
        path = Path(path)
    return path.expanduser().resolve()


def yield_dirs(path: Path) -> Iterator[Path]:
    """Recursively yield directories starting from `path`"""
    for entry in path.iterdir():
        if entry.is_dir():
            yield from yield_dirs(entry)
            yield entry


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


def generate_manifest(
    start_dir: Path, output_directory: Path, extensions: Iterable[str]
):
    return sorted(filepaths_with_extensions(start_dir, extensions))


def build_output_directory(
    base_output_directory: Path, starting_directory: Path
) -> Path:
    return base_output_directory / today2ymd() / starting_directory.name


def remove_directory_with_files_matching_extensions(
    directory: Path,
    extensions: set[str],
    logger: logging.Logger,
    *,
    dry_run: bool = True,
):
    """Remove a directory and all files within it which match `extensions`."""
    filepaths = sorted(scantree(directory))
    n_files = len(filepaths)

    # TODO: if n_files > threshold then switch to interactive & require input
    logger.debug(f"⚠️  Found {n_files} files to be deleted in {pathify(directory)!s}")

    # check that all files match extensions
    if additional_extensions := ({f.suffix for f in filepaths} - extensions):
        raise ValueError(
            f"Found additional extensions in {directory}. Ensure that any files matching extensions {additional_extensions} are removed."
        )

    if not dry_run:
        logger.debug(f"🗑️  Removing {n_files} files in {pathify(directory)!s}")
        shutil.rmtree(directory)


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
