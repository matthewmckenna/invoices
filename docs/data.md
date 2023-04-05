# Data

This section will detail the initial data gathering process, and how this can be reproduced.

## Data Extraction

The first stage of this process is to extract all possible invoice documents.

We will use the `dump-documents` command to do this.
This command will extract all `.doc` and `.docx` files from the given directory, and all subdirectories.
The directory structure will be preserved in the output directory.

```zsh
❯ invoicetool dump-documents --help
Usage: invoicetool dump-documents [OPTIONS] START_DIR

  Search for & copy Word documents

Options:
  -o, --output-directory DIRECTORY
  -a, --archive                   create a compressed archive
  -c, --config FILE               path to config file  [default:
                                  ./config.toml]
  --help                          Show this message and exit.
```

We can run using the defaults specified in `config.toml`.

```zsh
❯ invoicetool dump-documents START_DIR
```

The default working directory is `~/.invoicetool`.

## Hashes

To generate hashes for all documents, we can use the `hashes` command.

```zsh
❯ invoicetool hashes --help
Usage: invoicetool hashes [OPTIONS] START_DIR

  Compute the hashes of Word documents

Options:
  -a, --algorithm [MD5|SHA1|SHA256|SHA512]
                                  algorithm to use for the hash function
  -c, --config FILE               path to config file  [default:
                                  ./config.toml]
  --help                          Show this message and exit.
```

This command will produce two output files: `hashes.json` and `duplicates.json`.
The output files will be located in the **parent directory** passed at the command line.

As an example, if `~/.invoicetool/2023-04-05/books` was passed as the `START_DIR` as shown below:

```zsh
❯ invoicetool hashes ~/.invoicetool/2023-04-05/books
```

then the two output files would be located in `~/.invoicetool/2023-04-05`.

### Defaults

The default hash function algorithm used is `SHA1`.
This can be configured in `config.toml` with the `hash_function_algorithm` option.

Alternatively, you can use the `-a` or `--algorithm` option to specify the algorithm at the command line.

Both the config file and command line options are case insensitive, meaning you can pass your choice in upper or lower case.

```toml
hash_function_algorithm = "sha1"
```

## Data Cleaning

The next stage is to clean the data.

We will use the `clean-documents` command to do this.
