PYTHON ?= python

.PHONY: generate lint typecheck test build clean

generate:
	$(PYTHON) scripts/generate.py

lint:
	ruff check .

typecheck:
	mypy crawlforge scripts

test:
	pytest

build:
	$(PYTHON) -m build

clean:
	rm -rf dist build *.egg-info .pytest_cache .mypy_cache .ruff_cache
