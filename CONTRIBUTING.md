# Contributing to FastKit

Thank you for your interest in contributing to FastKit! This document provides guidelines for contributing to the project.

## Development Setup

1. Clone the repository
2. Install dependencies: `poetry install`
3. Run tests: `pytest`
4. Run linting: `ruff check`

## Project Structure

- `fastkit/cli/` - CLI interface and commands
- `fastkit/generators/` - Code generation logic
- `fastkit/templates/` - Jinja2 templates
- `fastkit/core/` - Core functionality
- `fastkit/utils/` - Utility functions
- `tests/` - Test suite

## Adding New Integrations

1. Create generator in `fastkit/generators/`
2. Add templates in `fastkit/templates/`
3. Update CLI commands
4. Add tests
5. Update documentation

## Code Style

- Use Black for formatting
- Use Ruff for linting
- Follow PEP 8
- Add type hints
- Write docstrings

## Testing

- Write unit tests for all new functionality
- Add integration tests for complex features
- Ensure all tests pass before submitting PR