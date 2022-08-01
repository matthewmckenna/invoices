# invoicesdb

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## TODO

- [x] upgrade project to 3.11.0b3


## Installation

This project is being built with **Python 3.11.0b3**.

To install the project, clone the repository & navigate to the directory.

**Note: This project uses `poetry` and the user will need to install this prior to running `make install`.**
  - See `howto.md`

```zsh
git clone git@github.com:matthewmckenna/invoices.git
cd invoices/
make install
```

## Plan

The current plan is to create a number of command-line tools (or a single tool with multiple subcommands) which will
  - Find all files with a given extension
  - Create a "manifest" as an intermediate file
  - Filter out duplicates
    - There are a number of duplicate files
    - There are a number of files which are very similar, but may have some extra information at the end
  - Filter out temporary Word docs, and empty documents

We've created a script (?) which calls:
  - package: invoicedb
  - module: cli.py
  - function: main

```toml
[tool.poetry.scripts]
# package, module, function
invoicedb = "invoicedb.cli:main"
```

## Usage

We can use this tool on the command line as follows:

```zsh
poetry run invoicedb
```

### Run Tests

To run the test suite:

```zsh
make test
```

## Development

### Add a dependency

```zsh
poetry add {dependency}
```

### Add a development dependency

```zsh
poetry add {dependency} --dev
```

## Installing using pip

**TODO: decide on how to include requirements.txt**
  - Maybe use `pip-tools`

```zsh
python -m pip install -r requirements.txt
```
