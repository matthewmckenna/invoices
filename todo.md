# TODO

## `invoicetool`

- [ ] calculate checksum for all files
- [ ] detect duplicate files
- [ ] create report for duplicates
- [ ] interactive session to choose which files to keep
- [ ] `archive` command
  - used to archive / checkpoint the state of the working directory

## README

- [x] add badges
- [ ] update e2e example for `dump-documents` to reflect date (YYYY-MM-DD) in the output directory

## `dump-documents`

### `archive` option

- [ ] configure archive compression format via config file
- [ ] configure archive compression format via command line option
- [ ] remove uncompressed document dump from working directory
  - if we use the `-a` flag then we don't want to leave the uncompressed files in the working directory
