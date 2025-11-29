# Flask-Mailing v3.0.0 - Development Makefile

sources = flask_mailing
tests = tests

.PHONY: all test format lint unittest coverage pre-commit clean install dev-install type-check

all: format lint test

# Install dependencies
install:
	pip install -e .

dev-install:
	pip install -e ".[dev,email-checking]"

# Code formatting
format:
	isort $(sources) $(tests)
	black $(sources) $(tests)

# Linting
lint:
	ruff check $(sources) $(tests)

type-check:
	mypy $(sources)

# Testing
unittest:
	pytest $(tests) -v

test: format lint unittest

coverage:
	pytest -s --cov=$(sources) --cov-append --cov-report=term-missing --cov-report=html $(tests)

# Pre-commit hooks
pre-commit:
	pre-commit run --all-files

# Cleanup
clean:
	rm -rf .pytest_cache
	rm -rf *.egg-info
	rm -rf .tox dist site build
	rm -rf coverage.xml .coverage htmlcov
	rm -rf .mypy_cache .ruff_cache
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true

# Build package
build: clean
	pip install build
	python -m build

# Documentation
docs:
	mkdocs serve

docs-build:
	mkdocs build --clean