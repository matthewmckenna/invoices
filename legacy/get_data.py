from pathlib import Path
import shutil
from typing import Iterable, Iterator, Union


def main():
    # first read the filelist from disk
    filepaths = list(yield_filepaths('data/invoices.txt'))
    # set up the destination directory
    # TODO: automatically add date to the destination
    destination = Path('~/mmk/invoices_2021-10-23').expanduser()

    # copy the files into `destination`
    copy_files(destination, filepaths)
    print(f'copied {len(filepaths)} documents to {destination}')

    archive_path = shutil.make_archive(
        base_name=destination,
        format='gztar',
        root_dir=destination,
    )
    print(f'created archive: {archive_path}')


def yield_filepaths(filepath: Union[str, Path]) -> Iterator[str]:
    """yield Path objects from a manifest file `filepath`"""
    with open(filepath, 'rt') as f:
        for line in f:
            yield Path(line.strip()).expanduser()


def copy_files(destination: Path, filepaths: Iterable[Path]):
    """
    copy files in `filepaths` from `source` to `destination`.

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


if __name__ == '__main__':
    main()
