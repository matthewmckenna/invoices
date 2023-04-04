.PHONY: black black-check clean flake8 format install isort isort-check test

SHELL := bash
.ONESHELL:
.DELETE_ON_ERROR:
.SHELLFLAGS := -eu -o pipefail -c
MAKEFLAGS += --warn-undefined-variables
MAKEFLAGS += --no-builtin-rules

SRC_PYTHON := /Users/matthew/.pyenv/versions/3.11.2/bin/python

PROJECT_NAME := invoicetool
SRC_DIR := src/$(PROJECT_NAME)
TESTS_DIR := tests
VENV_DIR := .venv
EGG_INFO_DIR := src/$(PROJECT_NAME).egg-info

ISORT := isort --profile black

VENV_PIP := $(VENV_DIR)/bin/pip
VENV_PYTHON := $(VENV_DIR)/bin/python

black:
	black $(SRC_DIR) $(TESTS_DIR) --preview

black-check:
	black $(SRC_DIR) $(TESTS_DIR) --check --diff --color --preview -v

check: black-check

clean:
	rm -r $(SRC_DIR)/__pycache__
	rm -r $(TESTS_DIR)/__pycache__
	rm -r $(EGG_INFO_DIR)

clean-logs:
	rm -r logs/*.log

coverage:
	pytest $(TESTS_DIR) --cov
	open .out/htmlcov/index.html

flake8:
	flake8 $(SRC_DIR) $(TESTS_DIR)

format: isort black

install:
	rm -r $(VENV_DIR)
	$(SRC_PYTHON) -m venv $(VENV_DIR)
	$(VENV_PIP) install --upgrade pip
	$(VENV_PIP) install --editable .[dev]

isort:
	$(ISORT) $(SRC_DIR) $(TESTS_DIR)

isort-check:
	$(ISORT) --check $(SRC_DIR) $(TESTS_DIR)

test:
	pytest $(TESTS_DIR)
