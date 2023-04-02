.PHONY: black black-check clean flake8 format install isort isort-check test

SRC_PYTHON := /Users/matthew/.pyenv/versions/3.11.2/bin/python
SRC_DIR := src/invoices
TESTS_DIR := tests
VENV_DIR := .venv
ISORT := isort --profile black
EGG_INFO_DIR := $(SRC_DIR)/invoices.egg-info

VENV_PIP := $(VENV_DIR)/bin/pip
VENV_PYTHON := $(VENV_DIR)/bin/python

black:
	black $(SRC_DIR) $(TESTS_DIR) --preview

black-check:
	black $(SRC_DIR) $(TESTS_DIR) --check --diff --color --preview -v

check: black-check

clean:
	rm -rf $(SRC_DIR)/__pycache__
	rm -rf $(TESTS_DIR)/__pycache__
	rm -rf $(EGG_INFO_DIR)

flake8:
	flake8 $(SRC_DIR) $(TESTS_DIR)

format: isort black

install:
	rm -rf $(VENV_DIR)
	$(SRC_PYTHON) -m venv $(VENV_DIR)
	$(VENV_PIP) install --upgrade pip
	$(VENV_PIP) install --editable .[dev]

isort:
	$(ISORT) $(SRC_DIR) $(TESTS_DIR)

isort-check:
	$(ISORT) --check $(SRC_DIR) $(TESTS_DIR)

test:
	pytest $(TESTS_DIR)
