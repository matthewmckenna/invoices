# import pytest
from invoicetool.iotools import ensure_path


def test_ensure_path_new_directory(tmp_path):
    path = ensure_path(tmp_path / "new_directory")
    assert path.exists()
    assert path.is_dir()


def test_ensure_path_existing_directory(tmp_path):
    path = ensure_path(tmp_path)
    assert path.exists()
    assert path.is_dir()


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
