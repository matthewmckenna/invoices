def test_extract_text_from_doc():
    # Test with a valid `.doc` file
    filepath = "path/to/valid/document.doc"
    expected_output = "This is the extracted text."
    assert extract_text_from_doc(filepath) == expected_output

    # Test with a non-existent file
    filepath = "path/to/nonexistent/file.doc"
    with pytest.raises(ValueError):
        extract_text_from_doc(filepath)

    # Test with a file that is not a `.doc` file
    filepath = "path/to/invalid/document.txt"
    with pytest.raises(ValueError):
        extract_text_from_doc(filepath)
