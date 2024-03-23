# Examples

## E2E Example: `dump-documents`

Here's an end-to-end example using the `dump-documents` command.

The `dump-documents` command accepts a starting directory (`START_DIR`) and recursively searches for all files which match extensions specified in `extensions`.
By default, the tool will look for Word documents with the following file extensions: `{.doc, .docx}`.

`books` is a sample directory containing a few Word documents and Excel spreadsheets:

```zsh
❯ tree books
books
├── another-level
│   ├── document03.doc
│   └── spreadsheet02.xlsx
├── doc02.docx
├── document01.doc
└── spreadsheet01.xls
```

Run the `dump-documents` command:

```zsh
❯ invoicetool dump-documents --output-directory ~/document-dumps data/books
```

We can go to the `--output-directory` specified above (`~/document-dumps`), and see that the directory structure has been mirrored.

Note that only the Word documents have been copied, and the Excel spreadsheets were ignored as we did not specify to include the extensions `.xls` or `.xlsx`.

```zsh
❯ cd ~
❯ tree document-dumps
document-dumps
└── 2023-04-11
    └── books
        ├── another-level
        │   └── document03.doc
        ├── doc02.docx
        └── document01.doc
```
