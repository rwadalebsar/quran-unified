# Contributing to Quran Unified

Thank you for your interest in contributing to `quran-unified`! This guide will help you get started.

## Code of Conduct

Please be respectful and considerate in all interactions. This project serves the Muslim community, and we expect all contributors to maintain a respectful and professional environment.

## Getting Started

### 1. Fork and Clone

```bash
# Fork the repository on GitHub, then clone your fork
git clone https://github.com/YOUR_USERNAME/quran-unified.git
cd quran-unified
```

### 2. Set Up Development Environment

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -e ".[dev]"
```

### 3. Create a Branch

```bash
git checkout -b feature/your-feature-name
```

## Development Workflow

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=quran_unified --cov-report=html

# Run specific test file
pytest tests/test_api.py

# Run specific test
pytest tests/test_api.py::TestQuranAPIValidation::test_invalid_surah_too_high
```

### Code Quality

```bash
# Format code with black
black src/ tests/

# Sort imports
isort src/ tests/

# Lint with ruff
ruff check src/ tests/

# Type checking
mypy src/quran_unified
```

### Pre-Commit Checklist

Before committing, ensure:

1. All tests pass: `pytest`
2. Code is formatted: `black src/ tests/`
3. Imports are sorted: `isort src/ tests/`
4. No lint errors: `ruff check src/ tests/`
5. Type hints are valid: `mypy src/quran_unified`

## Making Changes

### Adding a New Feature

1. Write tests first (TDD approach recommended)
2. Implement the feature
3. Update documentation if needed
4. Add an entry to CHANGELOG.md

### Fixing a Bug

1. Add a test that reproduces the bug
2. Fix the bug
3. Verify the test passes
4. Add an entry to CHANGELOG.md

### Adding a New API Client

If you want to add support for a new Quran data source:

1. Create a new client file in `src/quran_unified/clients/`
2. Extend the `BaseClient` class
3. Add the client to `src/quran_unified/clients/__init__.py`
4. Integrate with `QuranAPI` if needed
5. Add tests in `tests/test_clients/`
6. Update documentation

Example structure:

```python
# src/quran_unified/clients/new_source.py
from quran_unified.clients.base import BaseClient

class NewSourceClient(BaseClient):
    """Client for New Source API."""

    BASE_URL = "https://api.newsource.com/v1"

    def get_verse(self, surah: int, ayah: int) -> Dict:
        """Get verse from new source."""
        return self._get(f"/verse/{surah}/{ayah}")
```

## Project Structure

```
quran-unified/
├── src/quran_unified/
│   ├── __init__.py          # Package exports
│   ├── api.py                # Main QuranAPI class
│   ├── cli.py                # CLI commands
│   ├── exceptions.py         # Custom exceptions
│   ├── clients/              # API clients
│   │   ├── base.py           # Base client class
│   │   ├── alquran_cloud.py
│   │   ├── quran_com.py
│   │   ├── quranenc.py
│   │   ├── tafseer_api.py
│   │   └── everyayah.py
│   ├── models/               # Data models
│   │   ├── verse.py
│   │   ├── surah.py
│   │   ├── tafsir.py
│   │   └── reciter.py
│   ├── cache/                # Cache backends
│   │   ├── base.py
│   │   ├── memory.py
│   │   └── sqlite.py
│   └── utils/
│       └── constants.py      # Surah data, reciters
├── tests/                    # Test files
├── docs/                     # Documentation
├── examples/                 # Example scripts
└── pyproject.toml            # Project configuration
```

## Commit Guidelines

### Commit Message Format

```
type: short description

Longer description if needed.
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `test`: Adding or updating tests
- `refactor`: Code refactoring
- `style`: Formatting, missing semicolons, etc.
- `chore`: Maintenance tasks

**Examples:**
```
feat: add word-by-word translation support

fix: handle empty tafsir response from API

docs: add CLI examples to README

test: add tests for cache expiration
```

## Pull Request Process

1. Update documentation if you changed public APIs
2. Add tests for new functionality
3. Ensure all tests pass
4. Update CHANGELOG.md
5. Create a pull request with a clear description

### Pull Request Template

```markdown
## Description
Brief description of changes.

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Refactoring

## Checklist
- [ ] Tests pass locally
- [ ] Code is formatted with black
- [ ] Documentation updated
- [ ] CHANGELOG.md updated
```

## Reporting Issues

### Bug Reports

Include:
- Python version
- Package version
- Minimal reproducible example
- Expected vs actual behavior
- Error messages/stack traces

### Feature Requests

Include:
- Clear description of the feature
- Use case / motivation
- Example API if applicable

## Questions?

Feel free to open an issue for questions or discussions.

---

Thank you for contributing to `quran-unified`! May Allah reward your efforts.
