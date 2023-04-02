.PHONY: black black-check clean install

POETRY := $(shell command -v poetry 2> /dev/null)
VENV := .venv/

black:
	black invoicedb tests --preview

black-check:
	black invoicedb tests --check --diff --color -v

check: black-check

clean:
	rm -rf invoicedb/__pycache__
	rm -rf tests/__pycache__

install:
	rm -rf $(VENV)
	$(POETRY) config virtualenvs.in-project true
	$(POETRY) env use `pyenv which python`
	$(POETRY) run python -m pip install --upgrade pip setuptools
	$(POETRY) install

test:
	$(POETRY) run pytest tests
