#!/usr/bin/env python
"""generate a directory listing of files"""
import argparse
from datetime import date
from pathlib import Path
from typing import Iterable, Iterator

from get_duplicates import scantree


def get_filepaths_with_extension(directory: Path, extensions: Iterable[str]) -> Iterator[str]:
    """starting from `directory` yield filepaths matching any extension in `extensions`"""
    for entry in scantree(directory):
        p = Path(entry.path)

        if p.suffix in extensions:
            yield p.as_posix()


def main(args):
    """main entry point for the script"""
    directory = Path(args.directory)

    # file extensions we're interested in
    # TODO: use `args.extension`
    extensions = {'.doc', '.docx'}

    # get the date in YYYY-MM-DD
    today = date.today().isoformat()

    manifest = sorted(get_filepaths_with_extension(directory, extensions))

    with open(f'data/manifest_{today}.txt', 'wt') as f:
        f.write('\n'.join(filepath for filepath in manifest))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='find duplicate files in a given directory',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument('directory', help='starting directory')
    args = parser.parse_args()
    main(args)
