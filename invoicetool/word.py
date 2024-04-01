import subprocess
from pathlib import Path
from typing import Iterator

from docx import Document


def get_paragraphs(doc: Document) -> Iterator[str]:
    """get all paragraphs from a docx document"""
    for paragraph in doc.paragraphs:
        p = paragraph.text.strip()
        if not p:
            continue
        yield " ".join(p.split())


def extract_text_from_document_as_list(filepath: Path) -> list[str]:
    """Extract all text from a document and return the text as a list of paragraphs"""
    if filepath.suffix == ".docx":
        return extract_text_from_docx_as_list(filepath)
    elif filepath.suffix == ".doc":
        return extract_text_from_doc_as_list(filepath)
    else:
        raise ValueError(f"Unsupported file extension: {filepath.suffix}")


def extract_text_from_docx_as_list(filepath: Path) -> list[str]:
    """Extract all text from a `.docx` file and return a list of paragraphs"""
    text = extract_text_from_docx(filepath)
    return text_to_paragraphs(text)


def extract_text_from_doc_as_list(filepath: Path) -> list[str]:
    """Extract all text from a `.doc` file and return the text"""
    text = extract_text_from_doc(filepath)
    return text_to_paragraphs(text)


def text_to_paragraphs(text: str) -> list[str]:
    """Convert a string of text into a list of paragraphs"""
    return [p for p in text.split("\n") if p]


def extract_text_from_document(filepath: Path) -> str:
    """Extract all text from a document and return the text"""
    if filepath.suffix == ".docx":
        return extract_text_from_docx(filepath)
    elif filepath.suffix == ".doc":
        return extract_text_from_doc(filepath)
    else:
        raise ValueError(f"Unsupported file extension: {filepath.suffix}")


def extract_text_from_docx(filepath: Path) -> str:
    """Extract all text from a `.docx` file and return the text"""
    doc = Document(filepath)
    text = "\n".join(get_paragraphs(doc))
    return text


def extract_text_from_doc(filepath: Path) -> str:
    """Extract all text from a `.doc` file and return the text"""
    # process is the completed process
    process = subprocess.run(
        ["antiword", filepath.as_posix()],
        capture_output=True,
        text=True,
    )
    raw_text = process.stdout
    return raw_text.strip()
