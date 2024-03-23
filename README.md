# Invoice Tool

![Dynamic TOML Badge](https://img.shields.io/badge/dynamic/toml?url=https%3A%2F%2Fraw.githubusercontent.com%2Fmatthewmckenna%2Finvoices%2Fmmk%2F2024-03-refresh%2Fpyproject.toml&query=%24.project.version&label=version)

This project contains a number of utilities for creating an invoices database.


## Installation

This project is built with **Python 3.12.2**.

The project can be installed by running:

```shell
pyenv shell 3.12.2
uv venv
source .venv/bin/activate
uv pip install -e '.[dev]'
uv pip compile --generate-hashes pyproject.toml -o requirements.txt
uv pip compile --extra dev --generate-hashes pyproject.toml -o requirements-dev.txt
```


## Design

Goal: Create one-or-more command-line tools to accomplish the following tasks

### Acceptance criteria

- [x] Given a starting directory, find all files with a specific set of extensions
  - [x] Filter out temporary Word documents (i.e., name begins with `~$` and the file size is `162 B`)
- [x] Find duplicate files using the reverse mapping of filepath to hash
  - [ ] Generate a report of the duplicate files
  - [ ] Create a `WordFile` dataclass to represent a Word document
    - Attributes:
      - [ ] File size
      - [ ] Creation date
      - [ ] Last modified date
  - [ ] Figure out how to make a decision on which duplicate to keep


## Usage

```zsh
❯ invoicetool
Usage: invoicetool [OPTIONS] COMMAND [ARGS]...

  CLI tools for creating and working with an invoices database

Options:
  --version  Show the version and exit.
  --help     Show this message and exit.

Commands:
  dump-documents  Search for & copy Word documents
  hashes          Compute the hashes of Word documents
```

### Version

To get the version:

```zsh
❯ invoicetool --version
invoicetool, version 0.1.0
```

### Generate hashes & find duplicates

To calculate hashes for all files which match `extensions` starting at `START_DIR` (default: `.doc` and `.docx`), run:

```zsh
❯ invoicetool hashes START_DIR
```

### Dump documents

To dump all files which match `extensions` starting at `START_DIR` (default: `.doc` and `.docx`), run:

```zsh
❯ invoicetool dump-documents START_DIR
```

To create a compressed archive of the document dump use the `-a` or `--archive` option:

```zsh
❯ invoicetool dump-documents --archive START_DIR
```

#### Setting the document dump location

The **document dump location** is built from the `output_directory` and the current date.
The `output_directory` can be set in a few ways.
In order of precedence, the location can be set by:

1. Supplying the `-o` or `--output-directory` option to the `dump-documents` command
2. Setting the `base_output_directory` option in the `config.toml` file

If none of the above options are set, the `output_directory` defaults to: `~/.invoicetool`.

The **document dump location** is then constructed as:

```python
document_dump_location = output_directory / YYYY-MM-DD / START_DIR.name
```

where `START_DIR.name` is the final component of the `START_DIR` path.

#### Examples

This section demonstrates a few ways to set the document dump location.
To see a full end-to-end example of the `dump-documents` command see [this section](docs/examples.md#e2e-example-dump-documents).

Using the `-o` or `--output-directory` option at the command line:

```zsh
❯ invoicetool dump-documents --output-directory DOCUMENT_DUMP_LOCATION START_DIR
```

----

Using the `base_output_directory` option in the `config.toml` file:

```toml
[invoicetool]
base_output_directory = "DOCUMENT_DUMP_LOCATION"
```

## Development

### Formatting

To format the project using `ruff`:

```zsh
❯ make format
```

### Run tests

To run the tests using `pytest`:

```zsh
❯ make test
```
