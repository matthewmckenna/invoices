.PHONY: check clean clean-logs format sort test

SHELL := bash
.ONESHELL:
.DELETE_ON_ERROR:
.SHELLFLAGS := -eu -o pipefail -c
MAKEFLAGS += --warn-undefined-variables
MAKEFLAGS += --no-builtin-rules

PROJECT_NAME := invoicetool

SRC_DIR := $(PROJECT_NAME)
TEST_DIR := tests
VENV_DIR := .venv
EGG_INFO_DIR := $(PROJECT_NAME).egg-info

check:
	ruff check --output-format=full --extend-select I $(SRC_DIR) $(TEST_DIR)

clean:
	rm -rf $(SRC_DIR)/__pycache__
	rm -rf $(TEST_DIR)/__pycache__
	rm -rf $(EGG_INFO_DIR)
	rm -rf .out/
	rm -rf .pytest_cache/

clean-logs:
	rm -r logs/*.log

format: sort
	ruff format

sort:
	ruff check --select I --fix $(SRC_DIR) $(TEST_DIR)

test:
	pytest $(TEST_DIR)
