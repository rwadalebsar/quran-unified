# Quran Unified API - Requirements Specification
# For Claude Code Implementation

## Project Overview

Build a production-ready Python package called `quran-unified` that provides a single, unified interface to access multiple Quran data sources (text, translations, audio, tafsir).

---

## 1. Project Structure

```
quran-unified/
├── README.md
├── README_AR.md
├── LICENSE (MIT)
├── pyproject.toml
├── setup.py
├── requirements.txt
├── .gitignore
├── .github/
│   └── workflows/
│       ├── test.yml
│       └── publish.yml
├── src/
│   └── quran_unified/
│       ├── __init__.py
│       ├── api.py              # Main QuranAPI class
│       ├── clients/
│       │   ├── __init__.py
│       │   ├── base.py         # Base client class
│       │   ├── alquran_cloud.py
│       │   ├── quran_com.py
│       │   ├── tafseer_api.py
│       │   ├── everyayah.py
│       │   └── quranenc.py     # QuranEnc (islamiccontent.org) translations
│       ├── models/
│       │   ├── __init__.py
│       │   ├── verse.py
│       │   ├── surah.py
│       │   ├── tafsir.py
│       │   └── reciter.py
│       ├── cache/
│       │   ├── __init__.py
│       │   ├── memory.py
│       │   └── sqlite.py
│       ├── utils/
│       │   ├── __init__.py
│       │   └── constants.py    # Surah info, reciter mappings
│       ├── cli.py              # Command line interface
│       └── exceptions.py       # Custom exceptions
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_api.py
│   ├── test_clients/
│   │   ├── test_alquran_cloud.py
│   │   ├── test_quran_com.py
│   │   ├── test_tafseer_api.py
│   │   └── test_quranenc.py
│   ├── test_models.py
│   └── test_cache.py
├── examples/
│   ├── basic_usage.py
│   ├── batch_download.py
│   ├── export_json.py
│   └── async_example.py
└── docs/
    ├── index.md
    ├── quickstart.md
    ├── api_reference.md
    └── examples.md
```

---

## 2. Core Requirements

### 2.1 Data Models (`src/quran_unified/models/`)

#### Verse Model
```python
@dataclass
class Verse:
    surah: int                    # 1-114
    ayah: int                     # Ayah number in surah
    arabic_uthmani: str           # Uthmani script
    arabic_simple: str = ""       # Simple/Imlaei script
    arabic_tajweed: str = ""      # With tajweed markers (if available)
    translation: str = ""
    transliteration: str = ""
    audio_url: str = ""
    audio_urls: Dict[str, str] = field(default_factory=dict)  # Multiple reciters
    tafsir: str = ""
    word_by_word: List[Dict] = field(default_factory=list)
    
    # Metadata
    juz: int = 0
    hizb: int = 0
    hizb_quarter: int = 0
    ruku: int = 0
    manzil: int = 0
    page: int = 0                 # Madani mushaf page
    sajda: bool = False
    sajda_type: str = ""          # "recommended" or "obligatory"
    
    # Computed
    @property
    def reference(self) -> str:
        return f"{self.surah}:{self.ayah}"
    
    @property
    def verse_key(self) -> str:
        return f"{self.surah}:{self.ayah}"
    
    def to_dict(self) -> Dict[str, Any]: ...
    def to_json(self) -> str: ...
    
    @classmethod
    def from_dict(cls, data: Dict) -> "Verse": ...
```

#### Surah Model
```python
@dataclass
class Surah:
    number: int                          # 1-114
    name_arabic: str                     # الفاتحة
    name_english: str                    # The Opening
    name_transliteration: str            # Al-Fatihah
    verses_count: int
    revelation_type: RevelationType      # Enum: MECCAN, MEDINAN
    revelation_order: int
    pages: Tuple[int, int]               # Start and end pages
    
    # Optional loaded data
    verses: List[Verse] = field(default_factory=list)
    
    def to_dict(self) -> Dict: ...
    
    @classmethod
    def from_dict(cls, data: Dict) -> "Surah": ...
```

#### Tafsir Model
```python
@dataclass
class Tafsir:
    id: int
    name: str
    author: str
    language: str
    book_name: str = ""
    text: str = ""
    
    def to_dict(self) -> Dict: ...
```

#### Reciter Model
```python
@dataclass
class Reciter:
    id: str
    name_arabic: str
    name_english: str
    style: RecitationStyle      # Enum: MURATTAL, MUJAWWAD, MUALLIM
    bitrate: int = 128
    
    def to_dict(self) -> Dict: ...
```

### 2.2 API Clients (`src/quran_unified/clients/`)

#### Base Client
```python
class BaseClient:
    BASE_URL: str
    
    def __init__(self, timeout: int = 30, retries: int = 3):
        self.session = requests.Session()
        self.timeout = timeout
        self.retries = retries
    
    def _get(self, endpoint: str, params: Dict = None) -> Dict: ...
    def _handle_error(self, response: Response) -> None: ...
    
    def close(self) -> None: ...
    def __enter__(self) -> "BaseClient": ...
    def __exit__(self, *args) -> None: ...
```

#### AlQuran Cloud Client
```python
class AlQuranCloudClient(BaseClient):
    """
    API: https://alquran.cloud/api
    - No rate limits
    - Multiple editions support
    """
    
    BASE_URL = "https://api.alquran.cloud/v1"
    
    def get_verse(self, surah: int, ayah: int, edition: str = "quran-uthmani") -> Dict: ...
    def get_verse_multi(self, surah: int, ayah: int, editions: List[str]) -> Dict: ...
    def get_surah(self, surah: int, edition: str = "quran-uthmani") -> Dict: ...
    def get_juz(self, juz: int, edition: str = "quran-uthmani") -> Dict: ...
    def get_page(self, page: int, edition: str = "quran-uthmani") -> Dict: ...
    def get_editions(self, format: str = None, language: str = None, type: str = None) -> List[Dict]: ...
    def search(self, query: str, edition: str = "en.sahih", surah: int = None) -> Dict: ...
```

#### Quran.com Client
```python
class QuranComClient(BaseClient):
    """
    API: https://api.quran.com/api/v4
    - Rich metadata
    - Best search
    """
    
    BASE_URL = "https://api.quran.com/api/v4"
    
    def get_verse(self, surah: int, ayah: int, translations: str = None, fields: str = None) -> Dict: ...
    def get_verses_by_chapter(self, surah: int, translations: str = None, per_page: int = 50) -> Dict: ...
    def get_verses_by_juz(self, juz: int, translations: str = None) -> Dict: ...
    def get_verses_by_page(self, page: int, translations: str = None) -> Dict: ...
    def get_chapter(self, surah: int) -> Dict: ...
    def get_chapters(self) -> List[Dict]: ...
    def get_translations(self, language: str = "en") -> List[Dict]: ...
    def get_tafsirs(self, language: str = "en") -> List[Dict]: ...
    def get_reciters(self) -> List[Dict]: ...
    def search(self, query: str, language: str = "en", page: int = 1) -> Dict: ...
```

#### Tafseer API Client
```python
class TafseerAPIClient(BaseClient):
    """
    API: http://api.quran-tafseer.com
    - Arabic tafsirs
    """
    
    BASE_URL = "http://api.quran-tafseer.com"
    
    def get_tafsirs(self) -> List[Dict]: ...
    def get_tafsir(self, tafsir_id: int, surah: int, ayah: int) -> Dict: ...
    def get_tafsir_range(self, tafsir_id: int, surah: int, from_ayah: int, to_ayah: int) -> List[Dict]: ...
    def get_quran_text(self, surah: int, ayah: int) -> Dict: ...
```

#### EveryAyah Client
```python
class EveryAyahClient:
    """
    Audio URLs: https://everyayah.com/data/{reciter}/{surah:03d}{ayah:03d}.mp3
    """
    
    BASE_URL = "https://everyayah.com/data"
    
    RECITERS: Dict[str, str] = {
        "alafasy": "Alafasy_128kbps",
        "husary": "Husary_128kbps",
        "minshawi": "Minshawy_Murattal_128kbps",
        "sudais": "Abdurrahmaan_As-Sudais_192kbps",
        "abdulbasit": "Abdul_Basit_Murattal_192kbps",
        "ghamdi": "Ghamadi_40kbps",
        "ajamy": "Ahmed_ibn_Ali_al-Ajamy_128kbps_ketaballah.net",
        "muaiqly": "MasoodZaidi_128kbps",
        # ... add all 44 reciters
    }
    
    def get_audio_url(self, surah: int, ayah: int, reciter: str = "alafasy") -> str: ...
    def get_surah_audio_urls(self, surah: int, total_ayahs: int, reciter: str = "alafasy") -> List[str]: ...
    def get_available_reciters(self) -> List[str]: ...
```

#### QuranEnc Client
```python
class QuranEncClient(BaseClient):
    """
    API: https://quranenc.com/api/v1
    Operated by islamiccontent.org (جمعية خدمة المحتوى الإسلامي باللغات)
    - Encyclopedia of Quran translations
    - Translations with footnotes
    - Wide language coverage
    """

    BASE_URL = "https://quranenc.com/api/v1"

    def get_translations_list(self, language: str = None, localization: str = "en") -> List[Dict]:
        """
        List available translations, optionally filtered by language.
        GET /translations/list/[[{language}]]/?localization={localization}
        Returns: list of dicts with keys: key, language_iso_code, version, last_update, title, description
        """
        ...

    def get_sura_translation(self, translation_key: str, sura: int) -> List[Dict]:
        """
        Get translation for an entire surah.
        GET /translation/sura/{translation_key}/{sura_number}
        Returns: list of dicts with keys: sura, aya, translation, footnotes
        """
        ...

    def get_aya_translation(self, translation_key: str, sura: int, aya: int) -> Dict:
        """
        Get translation for a single ayah.
        GET /translation/aya/{translation_key}/{sura_number}/{aya_number}
        Returns: dict with keys: sura, aya, translation, footnotes
        """
        ...
```

### 2.3 Main API Class (`src/quran_unified/api.py`)

```python
class QuranAPI:
    """
    Unified interface for all Quran data sources.
    
    Example:
        quran = QuranAPI()
        verse = quran.get_verse(2, 255)
        print(verse.arabic_uthmani)
    """
    
    def __init__(
        self,
        default_translation: str = "en.sahih",
        default_reciter: str = "alafasy",
        default_tafsir: int = 1,
        cache_backend: str = "memory",  # "memory", "sqlite", "none"
        cache_ttl: int = 3600,
        timeout: int = 30,
        retries: int = 3
    ): ...
    
    # ==================== Verse Methods ====================
    
    def get_verse(
        self,
        surah: int,
        ayah: int,
        translation: str = None,
        reciter: str = None,
        include_tafsir: bool = False,
        tafsir_id: int = None,
        include_word_by_word: bool = False
    ) -> Verse: ...
    
    def get_verses(
        self,
        surah: int,
        from_ayah: int,
        to_ayah: int,
        translation: str = None,
        reciter: str = None
    ) -> List[Verse]: ...
    
    def get_random_verse(
        self,
        translation: str = None
    ) -> Verse: ...
    
    # ==================== Surah Methods ====================
    
    def get_surah(
        self,
        surah: int,
        translation: str = None,
        reciter: str = None,
        include_verses: bool = True
    ) -> Surah: ...
    
    def get_surah_info(self, surah: int) -> Surah: ...
    
    def get_all_surahs(self) -> List[Surah]: ...
    
    # ==================== Juz/Hizb/Page Methods ====================
    
    def get_juz(
        self,
        juz: int,
        translation: str = None
    ) -> List[Verse]: ...
    
    def get_hizb(
        self,
        hizb: int,
        translation: str = None
    ) -> List[Verse]: ...
    
    def get_page(
        self,
        page: int,
        translation: str = None
    ) -> List[Verse]: ...
    
    # ==================== Tafsir Methods ====================
    
    def get_tafsir(
        self,
        surah: int,
        ayah: int,
        tafsir_id: int = None
    ) -> Tafsir: ...
    
    def get_tafsir_range(
        self,
        surah: int,
        from_ayah: int,
        to_ayah: int,
        tafsir_id: int = None
    ) -> List[Tafsir]: ...
    
    def get_available_tafsirs(self) -> List[Tafsir]: ...
    
    # ==================== Audio Methods ====================
    
    def get_audio_url(
        self,
        surah: int,
        ayah: int,
        reciter: str = None
    ) -> str: ...
    
    def get_surah_audio_urls(
        self,
        surah: int,
        reciter: str = None
    ) -> List[str]: ...
    
    def get_available_reciters(self) -> List[Reciter]: ...
    
    # ==================== Search Methods ====================
    
    def search(
        self,
        query: str,
        language: str = "en",
        surah: int = None,
        limit: int = 50
    ) -> List[Verse]: ...
    
    # ==================== Translation Methods ====================
    
    def get_available_translations(
        self,
        language: str = None
    ) -> List[Dict]: ...
    
    # ==================== Utility Methods ====================
    
    def get_verse_count(self, surah: int) -> int: ...
    
    def clear_cache(self) -> None: ...
    
    def close(self) -> None: ...
    
    def __enter__(self) -> "QuranAPI": ...
    def __exit__(self, *args) -> None: ...
```

### 2.4 Cache System (`src/quran_unified/cache/`)

```python
# Base cache interface
class CacheBackend(ABC):
    @abstractmethod
    def get(self, key: str) -> Optional[Any]: ...
    
    @abstractmethod
    def set(self, key: str, value: Any, ttl: int = None) -> None: ...
    
    @abstractmethod
    def delete(self, key: str) -> None: ...
    
    @abstractmethod
    def clear(self) -> None: ...

# Memory cache
class MemoryCache(CacheBackend):
    def __init__(self, max_size: int = 1000): ...

# SQLite cache (for persistence)
class SQLiteCache(CacheBackend):
    def __init__(self, db_path: str = "~/.quran_unified/cache.db"): ...
```

### 2.5 CLI (`src/quran_unified/cli.py`)

```python
"""
Command Line Interface

Usage:
    quran verse 2:255
    quran verse 2:255 --translation en.sahih --json
    quran surah 1
    quran surah 1 --translation ar.muyassar
    quran search "الرحمن"
    quran tafsir 2:255 --tafsir-id 1
    quran audio 1:1 --reciter alafasy
    quran reciters
    quran translations --language ar
"""

import click

@click.group()
def cli(): ...

@cli.command()
@click.argument("reference")  # e.g., "2:255"
@click.option("--translation", "-t", default="en.sahih")
@click.option("--reciter", "-r", default="alafasy")
@click.option("--tafsir", is_flag=True)
@click.option("--json", is_flag=True)
def verse(reference, translation, reciter, tafsir, json): ...

@cli.command()
@click.argument("number", type=int)
@click.option("--translation", "-t", default="en.sahih")
@click.option("--json", is_flag=True)
def surah(number, translation, json): ...

@cli.command()
@click.argument("query")
@click.option("--language", "-l", default="en")
@click.option("--limit", default=10)
def search(query, language, limit): ...

@cli.command()
@click.argument("reference")
@click.option("--tafsir-id", "-i", default=1)
def tafsir(reference, tafsir_id): ...

@cli.command()
@click.argument("reference")
@click.option("--reciter", "-r", default="alafasy")
def audio(reference, reciter): ...

@cli.command()
def reciters(): ...

@cli.command()
@click.option("--language", "-l", default=None)
def translations(language): ...
```

### 2.6 Exceptions (`src/quran_unified/exceptions.py`)

```python
class QuranAPIError(Exception):
    """Base exception for Quran API errors"""
    pass

class InvalidReferenceError(QuranAPIError):
    """Invalid surah/ayah reference"""
    pass

class APIConnectionError(QuranAPIError):
    """Failed to connect to API"""
    pass

class RateLimitError(QuranAPIError):
    """API rate limit exceeded"""
    pass

class NotFoundError(QuranAPIError):
    """Resource not found"""
    pass

class CacheError(QuranAPIError):
    """Cache operation failed"""
    pass
```

---

## 3. Configuration Files

### 3.1 pyproject.toml

```toml
[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "quran-unified"
version = "0.1.0"
description = "Unified Python wrapper for multiple Quran data sources"
readme = "README.md"
license = {text = "MIT"}
authors = [
    {name = "Abdullah Alfadhli", email = "your@email.com"}
]
keywords = ["quran", "islam", "api", "arabic", "tafsir"]
classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Topic :: Religion",
    "Topic :: Software Development :: Libraries :: Python Modules",
]
requires-python = ">=3.8"
dependencies = [
    "requests>=2.28.0",
    "click>=8.0.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "pytest-cov>=4.0.0",
    "pytest-asyncio>=0.21.0",
    "responses>=0.23.0",
    "black>=23.0.0",
    "isort>=5.12.0",
    "mypy>=1.0.0",
    "ruff>=0.1.0",
]
async = [
    "aiohttp>=3.8.0",
    "aiofiles>=23.0.0",
]

[project.urls]
Homepage = "https://github.com/your-username/quran-unified"
Documentation = "https://quran-unified.readthedocs.io"
Repository = "https://github.com/your-username/quran-unified"
Issues = "https://github.com/your-username/quran-unified/issues"

[project.scripts]
quran = "quran_unified.cli:cli"

[tool.setuptools.packages.find]
where = ["src"]

[tool.black]
line-length = 100
target-version = ["py38", "py39", "py310", "py311", "py312"]

[tool.isort]
profile = "black"
line_length = 100

[tool.mypy]
python_version = "3.8"
warn_return_any = true
warn_unused_configs = true

[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "-v --cov=quran_unified --cov-report=term-missing"

[tool.ruff]
line-length = 100
select = ["E", "F", "W", "I", "N", "D", "UP", "B", "C4", "SIM"]
ignore = ["D100", "D104"]
```

### 3.2 requirements.txt

```
requests>=2.28.0
click>=8.0.0
```

### 3.3 .gitignore

```
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual environments
venv/
ENV/
env/
.venv/

# IDE
.idea/
.vscode/
*.swp
*.swo

# Testing
.coverage
htmlcov/
.pytest_cache/
.mypy_cache/

# Cache
.quran_unified/
*.db

# OS
.DS_Store
Thumbs.db
```

---

## 4. Testing Requirements

### 4.1 Test Coverage

- **Unit Tests**: All models, clients, cache
- **Integration Tests**: API endpoints (with mocking)
- **CLI Tests**: All commands
- **Minimum Coverage**: 80%

### 4.2 Test Files Structure

```python
# tests/conftest.py
import pytest
from quran_unified import QuranAPI

@pytest.fixture
def quran_api():
    return QuranAPI(cache_backend="none")

@pytest.fixture
def sample_verse_data():
    return {
        "surah": 1,
        "ayah": 1,
        "arabic_uthmani": "بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ",
        "translation": "In the name of Allah, the Entirely Merciful, the Especially Merciful."
    }

# tests/test_api.py
def test_get_verse(quran_api):
    verse = quran_api.get_verse(1, 1)
    assert verse.surah == 1
    assert verse.ayah == 1
    assert verse.arabic_uthmani != ""

def test_get_surah(quran_api):
    surah = quran_api.get_surah(1)
    assert surah.number == 1
    assert surah.verses_count == 7
    assert len(surah.verses) == 7

def test_search(quran_api):
    results = quran_api.search("الرحمن")
    assert len(results) > 0

def test_invalid_reference(quran_api):
    with pytest.raises(InvalidReferenceError):
        quran_api.get_verse(115, 1)  # Invalid surah
```

---

## 5. Documentation Requirements

### 5.1 README.md Content

1. Project description (English)
2. Installation instructions
3. Quick start examples
4. CLI usage
5. Configuration options
6. Contributing guide
7. License

### 5.2 README_AR.md Content

Same as English but in Arabic.

### 5.3 API Reference (docs/api_reference.md)

Full documentation of all classes and methods with examples.

---

## 6. GitHub Actions

### 6.1 test.yml

```yaml
name: Tests

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.8", "3.9", "3.10", "3.11", "3.12"]

    steps:
      - uses: actions/checkout@v4
      - name: Set up Python ${{ matrix.python-version }}
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
      - name: Install dependencies
        run: |
          pip install -e ".[dev]"
      - name: Run tests
        run: pytest
      - name: Upload coverage
        uses: codecov/codecov-action@v3
```

### 6.2 publish.yml

```yaml
name: Publish to PyPI

on:
  release:
    types: [published]

jobs:
  publish:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - name: Build package
        run: |
          pip install build
          python -m build
      - name: Publish to PyPI
        uses: pypa/gh-action-pypi-publish@release/v1
        with:
          password: ${{ secrets.PYPI_API_TOKEN }}
```

---

## 7. Implementation Order

1. **Phase 1**: Core structure
   - [ ] Create project structure
   - [ ] Implement models (Verse, Surah, Tafsir, Reciter)
   - [ ] Implement exceptions

2. **Phase 2**: Clients
   - [ ] Implement BaseClient
   - [ ] Implement AlQuranCloudClient
   - [ ] Implement QuranComClient
   - [ ] Implement TafseerAPIClient
   - [ ] Implement EveryAyahClient
   - [ ] Implement QuranEncClient

3. **Phase 3**: Main API
   - [ ] Implement QuranAPI class
   - [ ] Implement cache system
   - [ ] Add constants (surah info, reciters)

4. **Phase 4**: CLI & Tests
   - [ ] Implement CLI
   - [ ] Write unit tests
   - [ ] Write integration tests

5. **Phase 5**: Documentation & Publishing
   - [ ] Write README
   - [ ] Write API docs
   - [ ] Setup GitHub Actions
   - [ ] Publish to PyPI

---

## 8. Commands for Claude Code

```bash
# Start the project
"Create the quran-unified Python package following the requirements spec. Start with the project structure and core models."

# After structure is created
"Implement the API clients: AlQuranCloudClient, QuranComClient, TafseerAPIClient, and EveryAyahClient."

# After clients
"Implement the main QuranAPI class with caching support."

# After main API
"Implement the CLI using Click and add comprehensive tests."

# Final
"Add documentation, GitHub Actions workflows, and prepare for PyPI publishing."
```

---

## 9. Success Criteria

- [ ] All tests pass with 80%+ coverage
- [ ] CLI works correctly
- [ ] Documentation is complete
- [ ] Package installs via pip
- [ ] Works on Python 3.8-3.12
- [ ] No rate limit issues (uses AlQuran Cloud primarily)
- [ ] Response time < 2s for single verse

---

**Document Version**: 1.0
**Date**: January 2025
**Author**: Dr. Abdullah Alfadhli
