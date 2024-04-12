from pathlib import Path

import pytest

from invoicetool.iotools import (
    directory_is_empty,
    ensure_dir,
    get_relative_filepath,
    pathify,
    remove_empty_directories,
    yield_dirs,
)


def test_ensure_path_new_directory(tmp_path):
    path = tmp_path / "new_directory"
    ensure_dir(path)
    assert path.exists()
    assert path.is_dir()


def test_ensure_path_existing_directory(tmp_path):
    path = tmp_path
    ensure_dir(path)
    assert path.exists()
    assert path.is_dir()


@pytest.mark.parametrize(
    "path, expected",
    [
        ("~/test", Path.home() / "test"),
        ("~/test/../test/./", Path.home() / "test"),
        ("/non/existent/path", Path("/non/existent/path")),
    ],
)
def test_pathify(path, expected):
    assert pathify(path) == expected


def test_pathify_type():
    assert isinstance(pathify("~/test"), Path)


# def test_scantree(invoices_dir):
#     with tempfile.TemporaryDirectory() as tmpdirname:
#         # Create a directory with a nested subdirectory and some files
#         Path(tmpdirname + "/dir1/dir2").mkdir(parents=True, exist_ok=True)
#         Path(tmpdirname + "/file1.txt").write_text("file1 contents")
#         Path(tmpdirname + "/dir1/file2.txt").write_text("file2 contents")
#         Path(tmpdirname + "/dir1/dir2/file3.txt").write_text("file3 contents")

#         # Test scanning the directory tree for all files
#         filepaths = [str(p) for p in scantree(tmpdirname)]
#         assert set(filepaths) == set(
#             [
#                 tmpdirname + "/file1.txt",
#                 tmpdirname + "/dir1/file2.txt",
#                 tmpdirname + "/dir1/dir2/file3.txt",
#             ]
#         )


# def test_get_filepaths_of_interest():
#     with tempfile.TemporaryDirectory() as tmpdirname:
#         # Create a directory with some temporary MS Word files
#         Path(tmpdirname + "/~$temp1.doc").write_text("temporary file")
#         Path(tmpdirname + "/~$temp2.docx").write_text("temporary file")
#         Path(tmpdirname + "/file1.txt").write_text("file1 contents")
#         Path(tmpdirname + "/file2.pdf").write_text("file2 contents")

#         # Test getting the filepaths of interest
#         filepaths = [str(p) for p in get_filepaths_of_interest(tmpdirname, [".doc", ".docx"])]
#         assert set(filepaths) == set(
#             [
#                 tmpdirname + "/~$temp1.doc",
#                 tmpdirname + "/~$temp2.docx",
#             ]
#         )


# def test_remove_temporary_word_files():
#     with tempfile.TemporaryDirectory() as tmpdirname:
#         # Create a directory with some temporary MS Word files
#         Path(tmpdirname + "/~$temp1.doc").write_text("temporary file")
#         Path(tmpdirname + "/~$temp2.docx").write_text("temporary file")
#         Path(tmpdirname + "/file1.txt").write_text("file1 contents")
#         Path(tmpdirname + "/file2.pdf").write_text("file2 contents")

#         # Remove the temporary files
#         remove_temporary_word_files(tmpdirname, dry_run=False)

#         # Check that the temporary files were removed and the other files remain
#         assert set(os.listdir(tmpdirname)) == set(
#             [
#                 "file1.txt",
#                 "file2.pdf",
#             ]
#         )


# def test_is_empty_file():
#     with tempfile.TemporaryDirectory() as tmpdirname:
#         # Create a temporary MS Word file and a regular file
#         Path(tmpdirname + "/~$temp.doc").write_text("temporary file")
#         Path(tmpdirname + "/file1.txt").write_text("file1 contents")

#         # Test that the temporary MS Word file is detected as empty
#         assert is_empty_file(Path(tmpdirname + "/~$temp.doc")) == True

#         # Test that the regular file is not detected as empty


def test_directory_is_empty(empty_directory: Path, non_empty_directory: Path):
    assert directory_is_empty(empty_directory)
    assert not directory_is_empty(non_empty_directory)


def test_yield_dirs(empty_directory: Path, non_empty_directory: Path):
    dirs = list(yield_dirs(empty_directory))
    assert len(dirs) == 0

    dirs = list(yield_dirs(non_empty_directory))
    assert len(dirs) == 0


def test_remove_empty_directories(
    empty_directory: Path, non_empty_directory: Path, nested_empty_directories: Path
):
    remove_empty_directories(empty_directory)
    assert not empty_directory.exists()

    remove_empty_directories(non_empty_directory)
    assert non_empty_directory.exists()

    remove_empty_directories(nested_empty_directories)
    assert not nested_empty_directories.exists()


@pytest.mark.parametrize(
    "filepath, starting_directory, expected_filepath",
    [
        (Path("/Users/user/invoice.doc"), Path("/Users/user"), Path("invoice.doc")),
        (
            Path("/Users/user/2024/invoice3.docx"),
            Path("/Users/user"),
            Path("2024/invoice3.docx"),
        ),
        (
            Path("/Users/user/books/some_dir/invoice5.doc"),
            Path("/Users/user/books"),
            Path("some_dir/invoice5.doc"),
        ),
        (
            Path("/Volumes/External SSD/Archive/2021/invoice0.doc"),
            Path("/Volumes/External SSD"),
            Path("Archive/2021/invoice0.doc"),
        ),
        (
            Path("/Users/user/books/invoice-in-cwd.docx"),
            Path("/Users/user/books"),
            Path("invoice-in-cwd.docx"),
        ),
    ],
)
def test_get_relative_filepath(filepath, starting_directory, expected_filepath):
    assert get_relative_filepath(Path(filepath), str(starting_directory.name)) == expected_filepath
