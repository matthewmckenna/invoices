# Invoices

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
- Installs the `invoices` project in editable mode

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
invoices = "invoices.cli:cli"
```

## Usage

We can use this tool on the command line as follows:

```zsh
invoices
```

### Version

To get the version:

```zsh
invoices --version
invoices, version 0.1.0
```


### Dump Documents

To dump all `.doc` and `.docx` files starting at `START_DIR`, run:


```zsh
invoices dump-documents START_DIR
```

To also create a compressed archive of the dump with filename `YYYY-MM-DD.tar.bz2`, use the `-a` or `--archive` option:

```zsh
invoices dump-documents START_DIR --archive
```

The document dump location can be set in a number of ways:

1. By setting the `INVOICE_DB_DIR` environment variable
2. By supplying the `-d` or `--destination` argument

If the location is not set using one of the two options above, the fallback location is set as `~/invoicedb/YYYY-MM-DD`

#### Setting the document dump location

```zsh
invoices dump-documents START_DIR --destination DOCUMENT_DUMP_LOCATION
```
