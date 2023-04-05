import pytest

from invoicetool.word import extract_text_from_document, extract_text_from_docx


def test_extract_text_from_docx(docx_bytes):
    expected = "This is the first paragraph.\nThis is the second paragraph."
    assert extract_text_from_docx(docx_bytes) == expected


def test_extract_text_from_docx_non_existent_file(tmp_path):
    filepath = tmp_path / "nonexistent.docx"
    with pytest.raises(FileNotFoundError):
        extract_text_from_docx(filepath)


def test_extract_text_from_docx_not_a_docx_file(tmp_path):
    filepath = tmp_path / "document.txt"
    with pytest.raises(ValueError):
        extract_text_from_document(filepath)
