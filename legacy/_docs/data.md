# Data

## TODO

- [ ] Write Python code to generate the manifest
- [ ] Add command line argument for manifest
- [ ] Add command line argument for destination directory
- [ ] Update `find` command to use `fd`

## Data Extraction

This document will detail how the initial data was gathered, and how this can be reproduced.

### Generate a Manifest

Generate a manifest of all `{.doc, .docx}` files using the following command run from a terminal:

```zsh
$ find . -type f \( -name '*.doc' -o -name '*.docx' \) >~/manifest_2022-05-20.txt
$ head -n2 manifest_2022-05-20.txt
./Desktop/Echo Bank Lodgements/Statement Echo Electrodynamics 2020.docx
./Desktop/Echo Bank Lodgements/Echo Electrodynamics 2019 Payments.docx
```

### Clean the Manifest

The manifest will likely contain unwanted documents.

The notebook `manifest_analysis.ipynb` was used to clean the data, and produce `data/invoices.txt`.

`sed` was used to add `~/` to the start of each line:

```zsh
$ sed 's/^/~\//' data/invoices.txt >invoices_modified.txt
```

### Extract Data from Target

- Run `get_data.py` on the target machine.
- This script currently expects the filepaths (in the manifest file) to be in `data/invoices.txt`.
