# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

`quran-unified` is a Python package providing a single, unified interface to access multiple Quran data sources (text, translations, audio, tafsir). The project is **fully implemented** — see `REQUIREMENTS_SPEC.md` for the original specification.

## Build & Development Commands

```bash
# Install in development mode with all dev dependencies
pip install -e ".[dev]"

# Install async extras
pip install -e ".[async]"

# Run all tests with coverage
pytest

# Run a single test file
pytest tests/test_api.py

# Run a specific test
pytest tests/test_api.py::test_get_verse

# Linting and formatting
black src/ tests/
isort src/ tests/
ruff check src/ tests/
mypy src/

# Build the package
pip install build && python -m build
```

## Architecture

The package follows a **layered facade pattern** with five layers:

### 1. CLI Layer (`src/quran_unified/cli.py`)
Click-based CLI exposed as the `quran` command. Parses verse references in `surah:ayah` format (e.g., `2:255`).

### 2. Unified API Layer (`src/quran_unified/api.py`)
`QuranAPI` class is the main entry point and public facade. It orchestrates calls across multiple backend clients, merging results into unified data models. Supports context manager protocol. Configurable defaults: translation (`en.sahih`), reciter (`alafasy`), tafsir ID (`1`).

### 3. Client Layer (`src/quran_unified/clients/`)
Five API clients, all extending `BaseClient`:
- **AlQuranCloudClient** — `api.alquran.cloud/v1` — Primary source, no rate limits, multiple editions
- **QuranComClient** — `api.quran.com/api/v4` — Rich metadata, best search
- **TafseerAPIClient** — `api.quran-tafseer.com` — Arabic tafsirs
- **EveryAyahClient** — `everyayah.com/data` — Audio URLs for 44+ reciters (URL construction, no HTTP requests)
- **QuranEncClient** — `quranenc.com/api/v1` — Quran translations with footnotes, wide language coverage (operated by islamiccontent.org)

`BaseClient` manages HTTP sessions with configurable timeout/retries and context manager support.

### 4. Data Models (`src/quran_unified/models/`)
Dataclasses: `Verse`, `Surah`, `Tafsir`, `Reciter`. Each has `to_dict()`/`from_dict()` serialization. `Verse` carries text in multiple scripts (Uthmani, Simple, Tajweed), plus translation, audio, tafsir, and Quran division metadata (juz, hizb, page, ruku, manzil, sajda).

### 5. Cache Layer (`src/quran_unified/cache/`)
Abstract `CacheBackend` with three implementations: `MemoryCache` (LRU, max 1000 entries), `SQLiteCache` (persistent at `~/.quran_unified/cache.db`), and `NoCache`. Default TTL is 3600s.

### Exception Hierarchy (`src/quran_unified/exceptions.py`)
`QuranAPIError` base with: `InvalidReferenceError`, `APIConnectionError`, `RateLimitError`, `NotFoundError`, `CacheError`.

### Constants (`src/quran_unified/utils/constants.py`)
Surah metadata (names, verse counts, revelation info), reciter mappings (44+ reciters with file naming conventions), and Quran division boundaries (juz/hizb/page).

## Key Design Decisions

- **AlQuran Cloud is the primary data source** (no rate limits); Quran.com is secondary for richer metadata/search
- **EveryAyahClient** constructs audio URLs deterministically (`{base}/{reciter}/{surah:03d}{ayah:03d}.mp3`) rather than making API calls
- Python 3.8+ compatibility required — avoid walrus operator, `match` statements, and `type` aliases
- Async support is optional (via `aiohttp`/`aiofiles` extras), not required for core functionality
- `src/` layout with `setuptools` build backend and `pyproject.toml`

## Testing

- Framework: `pytest` with `pytest-cov`, `pytest-asyncio`, `responses` (HTTP mocking)
- Coverage target: 80%+
- Config in `pyproject.toml`: `testpaths = ["tests"]`, verbose + coverage enabled by default
- All API tests must mock HTTP calls using the `responses` library

## Code Style

- **black** formatter, line length 100
- **isort** with black profile
- **ruff** linter: rules E, F, W, I, N, D, UP, B, C4, SIM (D100/D104 ignored)
- **mypy** in Python 3.8 mode

## Implementation Phases

The spec defines five phases — follow this order:
1. Project structure + models + exceptions
2. API clients (Base → AlQuranCloud → Quran.com → Tafseer → EveryAyah → QuranEnc)
3. QuranAPI facade + cache system + constants
4. CLI + tests
5. Documentation + GitHub Actions + PyPI prep
