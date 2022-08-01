.PHONY: black black-check clean install

black:
	black invoicedb tests

black-check:
	black invoicedb tests --check --diff --color -v

clean:
	rm -rf invoicedb/__pycache__
	rm -rf tests/__pycache__

install:
	poetry config virtualenvs.in-project true
	poetry env use `pyenv which python`
	rm -rf .venv/
	poetry install

test:
	pytest tests
