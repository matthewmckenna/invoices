# Invoice Tool

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
![GitHub last commit (branch)](https://img.shields.io/github/last-commit/matthewmckenna/invoices/mmk/2023-04-refactor)
![GitHub pull requests](https://img.shields.io/github/issues-pr/matthewmckenna/invoices)
![GitHub issues](https://img.shields.io/github/issues/matthewmckenna/invoices)

This project contains a number of utilities for creating an invoices database.

## Installation

This project is built with **Python 3.11.2**.

The project can be installed by running:

```zsh
❯ git clone git@github.com:matthewmckenna/invoices.git invoicetool
❯ cd invoicetool
❯ make install
```

This will do the following:

- Clone the repository into local directory `invoicetool`
- Change directory into the newly cloned repository
- Remove any existing virtual environment (in `.venv`) if it exists
- Create a new virtual environment using Python 3.11.2
- Updates `pip` and `setuptools`
- Installs the `invoicetool` project in editable mode

## Design

Goal: Create one-or-more command-line tools to accomplish the following tasks

### Acceptance criteria
- [x] Given a starting directory, find all files with a specific set of extensions
  - [x] Filter temporary Word documents (i.e., name begins with `~$` and the file size is `162 B`
- [ ] Filter out duplicates
- [ ] Create a "manifest" as an intermediate file

## Usage

To activate the environent:

```zsh
❯ source .venv/bin/activate
```

Run the tool:

```zsh
❯ invoicetool
Usage: invoicetool [OPTIONS] COMMAND [ARGS]...

  CLI tools for creating and working with an invoices database

Options:
  --version  Show the version and exit.
  --help     Show this message and exit.

Commands:
  dump-documents  Search for & copy Word documents starting at `START_DIR`
```

### Version

To get the version:

```zsh
❯ invoicetool --version
invoicetool, version 0.1.0
```

### Dump documents

To dump all `.doc` and `.docx` files starting at `START_DIR`, run:

```zsh
❯ invoicetool dump-documents START_DIR
```

To also create a compressed archive of the dump with filename `YYYY-MM-DD.tar.bz2`, use the `-a` or `--archive` option:

```zsh
❯ invoicetool dump-documents --archive START_DIR
```

#### Setting the document dump location

The document dump location is constructed from the `working_directory` and the current date.
The `working_directory` can be set in a number of ways.
In order of precedence, the location can be set by:

1. Supplying the `-o` or `--output-directory` option to the `dump-documents` command
2. Setting the `INVOICETOOL_WORKING_DIR` environment variable
3. Setting the `working_directory` option in the `config.toml` file

If none of the above options are set, the `working_directory` is set to the fallback location: `~/.invoicetool`.

The document dump location is then constructed as:

```python
document_dump_location = working_directory / "YYYY-MM-DD"
```

#### Examples

This section demonstrates a number of ways to set the document dump location.
To see a full end-to-end example of the `dump-documents` command see [this section](docs/examples.md#e2e-example-dump-documents).

To set the document dump location using the `-d` or `--destination` option:

```zsh
❯ invoicetool dump-documents --destination DOCUMENT_DUMP_LOCATION START_DIR
```

----

To set the document dump location using the `INVOICETOOL_WORKING_DIR` environment variable:

```zsh
❯ export INVOICETOOL_WORKING_DIR=DOCUMENT_DUMP_LOCATION
❯ invoicetool dump-documents START_DIR
```

or to set the environment variable for the current session only:

```zsh
❯ INVOICETOOL_WORKING_DIR=DOCUMENT_DUMP_LOCATION invoicetool dump-documents START_DIR
```

----

To set the document dump location using the `working_directory` option in the `config.toml` file:

```toml
working_directory = "DOCUMENT_DUMP_LOCATION"
```

## Linting & Formatting

### Formatting

To format the source and tests:

```zsh
❯ make format
```

This will run `isort` and `black` on the source and tests.

### Run tests

To run the tests:

```zsh
❯ make test
```

This will run all tests within the `tests` directory.

### Coverage

To run the tests and generate a coverage report:

```zsh
❯ make coverage
```

Running `make coverage` will generate a coverage report in the `htmlcov` directory, and then open the report in the browser.
