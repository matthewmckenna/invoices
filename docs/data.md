# Data

This section will detail the initial data gathering process, and how this can be reproduced.

## Data Extraction

The first stage of this process is to extract all possible invoice documents.
We will use the `dump-documents` command to do this.

This command will extract all files which match the extensions specified in `extensions` (default: `.doc` and `.docx`) from the specified starting directory.
The directory structure will be preserved in the output document dump.

```zsh
❯ invoicetool dump-documents --help
Usage: invoicetool dump-documents [OPTIONS] START_DIR

  Search for & copy Word documents

Options:
  -o, --output-directory DIRECTORY
  -a, --archive                   create a compressed archive
  -c, --config FILE               path to config file
  --help                          Show this message and exit.
```

We can run using the defaults specified in `config.toml`.

```zsh
❯ invoicetool dump-documents START_DIR
```

### `-a / --archive`

To create a compressed archive of the document dump use the `-a` or `--archive` option.

```zsh
❯ invoicetool dump-documents --archive START_DIR
```

This will create a `.tar.bz2` archive of the document dump in `${OUTPUT_DIRECTORY}/${YYYY-MM-DD}`.

To inspect the contents of the example archive produced on `2024-03-23`:

```zsh
❯ tar tjf 2024-03-23/books.tar.bz2
./
./books/
./books/another-level/
./books/another-level/document03.doc
./books/doc02.docx
./books/document01.doc
```

### `-o / --output-directory`

```toml
[invoicetool]
# base output directory where the invoice database and document dumps will be located
base_output_directory = "~/.invoicetool"
```

The default output directory is `~/.invoicetool`.

This is set using the `base_output_directory` option in `config.toml`.
You can use the `-o` or `--output-directory` option to set the output directory at the command line.

### `-c / --config`

The default path to the config file is `./config.toml`.

You can specify a path to a different `TOML` config file using the `-c` or `--config` option.

```zsh
❯ invoicetool hashes --config /path/to/alternative/config.toml START_DIR
```

## Hashes

To generate hashes for all documents we can use the `hashes` command.

```zsh
❯ invoicetool hashes --help
Usage: invoicetool hashes [OPTIONS] START_DIR

  Compute the hashes of Word documents

Options:
  -a, --algorithm [MD5|SHA1|SHA256|SHA512]
                                  algorithm to use for the hash function
  -o, --output-directory DIRECTORY
  -c, --config FILE               path to config file
  --help                          Show this message and exit.
```

This command will produce two output files: `hashes.json` and `duplicates.json`.
These files will be located in: `${OUTPUT_DIRECTORY}/${YYYY-MM-DD}`

For example if we run the following command using the defaults:

```zsh
❯ invoicetool hashes ~/2024/books
```

then the output files will be located in `~/.invoicetool/${YYYY-MM-DD}`.

### `-o / --output-directory`

```toml
[invoicetool]
# base output directory where the invoice database and document dumps will be located
base_output_directory = "~/.invoicetool"
```

The default output directory is `~/.invoicetool`.

This is set using the `base_output_directory` option in `config.toml`.
You can use the `-o` or `--output-directory` option to set the output directory at the command line.

### `-a / --algorithm`

```toml
[invoicetool]
hash_function_algorithm = "sha1"
```

The default hash function algorithm used is `SHA1`.

This is set using the `hash_function_algorithm` option in `config.toml`.
Alternatively, you can use the `-a` or `--algorithm` option to specify the algorithm at the command line.

Both the config file and command line options are case insensitive, meaning you can pass your choice in upper or lower case. Valid options are: `MD5`, `SHA1`, `SHA256`, and `SHA512`.

### `-c / --config`

The default path to the config file is `./config.toml`.

You can specify a path to a different `TOML` config file using the `-c` or `--config` option.

```zsh
❯ invoicetool hashes --config /path/to/alternative/config.toml START_DIR
```


## Data Cleaning

The next stage is to clean the data.

We will use the `clean-documents` command to do this.
