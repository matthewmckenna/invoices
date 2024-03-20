# Refresh

Wed 20-Mar-2024

Pull request: https://github.com/matthewmckenna/invoices/pull/3

This is a short note about the branch `mmk/2024-03-refresh`.
The main goal of the refresh is to update the project so that I can start working on it again. A secondary goal is to improve the documentation and codebase.

## What does "update the project" mean?

- Update the Python version (`3.11` → `3.12`)
- Switch to `uv`
- Switch from `black`, `flake8`, and `isort` to `ruff`
- Update project dependencies
- Update the `Makefile`

## Goals

- [ ] Document the process of getting the initial document dump
- [ ] Document the deduplication process
- [ ] Improve / update the config file loading process
- [ ] Improve / update the logging implementation
