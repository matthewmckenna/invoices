from __future__ import annotations

import io
import subprocess
from pathlib import Path
from typing import Iterable

from docx import Document


def get_paragraphs(doc: Document) -> Iterable[str]:
    """get all paragraphs from a document"""
    for paragraph in doc.paragraphs:
        p = paragraph.text.strip()

        # get rid of blank lines
        if not p:
            continue

        # TODO: maybe call generic `sanitise` which
        # does multiple cleaning operations
        yield multi_whitespace_to_space(p)


def multi_whitespace_to_space(s: str) -> str:
    """squeeze multiple whitespace characters into a single space"""
    return " ".join(s.split())


def extract_text_from_docx_as_list(filepath: Path) -> list[str]:
    """Extract all text from a `.docx` file and return a list of paragraphs"""
    doc = Document(filepath)
    text_list = list(get_paragraphs(doc))
    return text_list


def extract_text_from_doc(filepath: Path) -> str:
    """Extract all text from a `.docx` file and return the text"""
    # process is the completed process
    process = subprocess.run(
        ["antiword", filepath.as_posix()],
        capture_output=True,
        text=True,
    )
    raw_text = process.stdout
    return multi_whitespace_to_space(raw_text)


def extract_text_from_docx(filepath: Path) -> str:
    """Extract all text from a `.docx` file and return the text"""
    doc = Document(filepath)
    text = "\n".join(get_paragraphs(doc))
    return text


def extract_text_from_document(filepath: Path) -> str:
    """Extract all text from a document and return the text"""
    if filepath.suffix == ".docx":
        return extract_text_from_docx(filepath)
    elif filepath.suffix == ".doc":
        return extract_text_from_doc(filepath)
    else:
        raise ValueError(f"Unsupported file extension: {filepath.suffix}")
