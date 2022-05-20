.PHONY: black black-check clean install

black:
	black invoicedb tests

black-check:
	black invoicedb tests --check --diff

clean:
	rm -rf __pycache__

install:
	poetry install
