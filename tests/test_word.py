from pathlib import Path

import pytest

from invoicetool.word import (
    extract_text_from_doc,
    extract_text_from_doc_as_list,
    extract_text_from_document,
    extract_text_from_docx_as_list,
    get_text_from_docx,
    text_to_paragraphs,
)

expected_older_format_text = """
This is a test document.
It has a second line here.

This could be a second paragraph.

Third.
"""

expected_newer_format_text = """
This is a test document.
It has a second line here.
This could be a second paragraph.
Third.
Four paragraphs in this doc, but the difference is this is a .docx.
"""


def test_extract_text_from_docx(docx_bytes):
    expected = "This is the first paragraph.\nThis is the second paragraph."
    assert get_text_from_docx(docx_bytes) == expected


def test_extract_text_from_docx_non_existent_file(tmp_path):
    filepath = tmp_path / "nonexistent.docx"
    with pytest.raises(FileNotFoundError):
        get_text_from_docx(filepath)


def test_extract_text_from_docx_not_a_docx_file(tmp_path):
    filepath = tmp_path / "document.txt"
    with pytest.raises(ValueError):
        extract_text_from_document(filepath)


def test_extract_text_from_docx_document(real_docx_filepath: Path):
    text = extract_text_from_document(real_docx_filepath)
    assert text == expected_newer_format_text.strip("\n")


def test_extract_text_as_list_from_docx_document(real_docx_filepath: Path):
    paragraphs = extract_text_from_docx_as_list(real_docx_filepath)
    expected_paragraphs = text_to_paragraphs(expected_newer_format_text)
    assert paragraphs == expected_paragraphs


def test_extract_text_from_doc_document(real_doc_filepath: Path):
    text = extract_text_from_doc(real_doc_filepath)
    assert text == expected_older_format_text.strip("\n")


def test_extract_text_as_list_from_doc_document(real_doc_filepath: Path):
    paragraphs = extract_text_from_doc_as_list(real_doc_filepath)
    expected_paragraphs = text_to_paragraphs(expected_older_format_text)
    assert paragraphs == expected_paragraphs
