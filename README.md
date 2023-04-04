# Invoice Tool

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

This project contains a number of utilities for creating an invoices database.

## Installation

This project is being built with **Python 3.11.2**.

To install the project, clone the repository, navigate to the repo, and run:

```zsh
git clone git@github.com:matthewmckenna/invoices.git
cd invoices
make install
```

This will do the following:

- Remove any existing virtual environment (in `.venv`) if it exists
- Create a new virtual environment using Python 3.11.2
- Updates `pip`
- Installs the `invoicetool` project in editable mode

### Activate the Environment

To activate the environent:

```zsh
source .venv/bin/activate
```

### Format the Project

To format the project, run:

```zsh
make format
```

This runs:
- `isort`
- `black`

### Run Tests

```zsh
make test
```

## Plan

The current plan is to create a number of command-line tools (or a single tool with multiple subcommands) which will:

- Find all files with a given extension
- Create a "manifest" as an intermediate file
- Filter out duplicates
  - There are a number of duplicate files
  - There are a number of files which are very similar, but may have some extra information at the end
- Filter out temporary Word docs, and empty documents

```toml
[project.scripts]
invoicetool = "invoicetool.cli:cli"
```

## Usage

We can use this tool on the command line as follows:

```zsh
invoicetool
```

### Version

To get the version:

```zsh
invoicetool --version
invoicetool, version 0.1.0
```


### Dump Documents

To dump all `.doc` and `.docx` files starting at `START_DIR`, run:


```zsh
invoicetool dump-documents START_DIR
```

To also create a compressed archive of the dump with filename `YYYY-MM-DD.tar.bz2`, use the `-a` or `--archive` option:

```zsh
invoicetool dump-documents START_DIR --archive
```

### Setting the document dump location

The document dump location can be set in a number of ways.
In order of precedence, the location can be set by:

1. By supplying the `-d` or `--destination` option to the `dump-documents` command
2. By setting the `INVOICETOOL_WORKING_DIR` environment variable
3. By setting the `working_directory` option in the `config.toml` file

If none of the above options are set, the fallback location is set as `~/.invoicetool/<YYYY-MM-DD>`

#### Examples

To set the document dump location using the `-d` or `--destination` option:

```zsh
invoicetool dump-documents START_DIR --destination DOCUMENT_DUMP_LOCATION
```

----

To set the document dump location using the `INVOICETOOL_WORKING_DIR` environment variable:

```zsh
export INVOICETOOL_WORKING_DIR=DOCUMENT_DUMP_LOCATION
invoicetool dump-documents START_DIR
```

or to set the environment variable for the current session only:

```zsh
INVOICETOOL_WORKING_DIR=DOCUMENT_DUMP_LOCATION invoicetool dump-documents START_DIR
```

----

To set the document dump location using the `working_directory` option in the `config.toml` file:

```toml
working_directory = "DOCUMENT_DUMP_LOCATION"
```


### E2E Example: `dump-documents`

Here's an end-to-end example using the `dump-documents` command of `invoicetool`.

The `dump-documents` command accepts a starting directory (`START_DIR`) and recursively searches for all files of specified type.
By default, the tool will look for Word documents: [`.doc`, `.docx`].

`books` is a sample directory containing a few Word documents and Excel spreadsheets:

```zsh
❯ tree books
books
├── another-level
│   ├── document03.doc
│   └── spreadsheet02.xlsx
├── document01.doc
├── document02.docx
└── spreadsheet01.xls
```

We run the `dump-documents` command:

```zsh
❯ invoicetool dump-documents books --output-directory ~/document-dumps
```

We can go to the `--output-directory` specified above (`~/document-dumps`) and see that the directory structure has been mirrored:

```zsh
❯ cd ~
❯ tree document-dumps
document-dumps
└── books
    ├── another-level
    │   ├── document03.doc
    │   └── spreadsheet02.xlsx
    ├── document01.doc
    ├── document02.docx
    └── spreadsheet01.xls
```
