# FastKit Makefile

.PHONY: install test lint format clean build publish

install:
	poetry install

test:
	pytest tests/ -v

test-cov:
	pytest tests/ --cov=fastkit --cov-report=html

lint:
	ruff check fastkit/ tests/
	mypy fastkit/

format:
	black fastkit/ tests/
	ruff check --fix fastkit/ tests/

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf htmlcov/
	find . -type d -name __pycache__ -delete
	find . -type f -name "*.pyc" -delete

build:
	poetry build

publish:
	poetry publish

dev-install:
	pip install -e .

help:
	@echo "Available commands:"
	@echo "  install     Install dependencies"
	@echo "  test        Run tests"
	@echo "  test-cov    Run tests with coverage"
	@echo "  lint        Run linting"
	@echo "  format      Format code"
	@echo "  clean       Clean build artifacts"
	@echo "  build       Build package"
	@echo "  publish     Publish to PyPI"
	@echo "  dev-install Install in development mode"