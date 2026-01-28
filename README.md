# Quran Unified

[![PyPI version](https://badge.fury.io/py/quran-unified.svg)](https://badge.fury.io/py/quran-unified)
[![Python Versions](https://img.shields.io/pypi/pyversions/quran-unified.svg)](https://pypi.org/project/quran-unified/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A unified Python wrapper for multiple Quran data sources. Access Quran text, translations, audio recitations, and tafsir (commentary) through a single, elegant API.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage Examples](#usage-examples)
  - [Getting Verses](#getting-verses)
  - [Getting Surahs](#getting-surahs)
  - [Audio Recitations](#audio-recitations)
  - [Tafsir (Commentary)](#tafsir-commentary)
  - [Search](#search)
- [Command Line Interface](#command-line-interface)
- [Configuration](#configuration)
- [Data Sources](#data-sources)
- [API Reference](#api-reference)
- [Contributing](#contributing)
- [License](#license)

## Features

- **Unified API** - Single interface to access data from 5 different sources
- **Multiple Text Formats** - Uthmani, Simple (Imlaei), and Tajweed scripts
- **100+ Translations** - Translations in 40+ languages
- **44+ Reciters** - Audio recitations from world-renowned Quran reciters
- **Tafsir Support** - Arabic tafsir/commentary from classical scholars
- **Smart Caching** - Built-in memory and SQLite caching for performance
- **CLI Tool** - Command-line interface for quick access
- **Type Hints** - Full type annotation support for IDE autocompletion
- **Python 3.8+** - Supports Python 3.8, 3.9, 3.10, 3.11, and 3.12

## Installation

### From PyPI (Recommended)

```bash
pip install quran-unified
```

### From GitHub

```bash
pip install git+https://github.com/rwadalebsar/quran-unified.git
```

### For Development

```bash
git clone https://github.com/rwadalebsar/quran-unified.git
cd quran-unified
pip install -e ".[dev]"
```

## Quick Start

```python
from quran_unified import QuranAPI

# Create an API instance
quran = QuranAPI()

# Get Ayat al-Kursi (2:255)
verse = quran.get_verse(2, 255)
print(f"Arabic: {verse.arabic_uthmani}")
print(f"Translation: {verse.translation}")
print(f"Audio: {verse.audio_url}")

# Always close when done (or use context manager)
quran.close()
```

### Using Context Manager (Recommended)

```python
from quran_unified import QuranAPI

with QuranAPI() as quran:
    # Get Al-Fatihah
    surah = quran.get_surah(1)
    print(f"{surah.name_english} ({surah.name_arabic})")
    print(f"Verses: {surah.verses_count}")

    for verse in surah.verses:
        print(f"  [{verse.ayah}] {verse.arabic_uthmani}")
```

## Usage Examples

### Getting Verses

```python
from quran_unified import QuranAPI

with QuranAPI() as quran:
    # Get a single verse
    verse = quran.get_verse(2, 255)
    print(verse.arabic_uthmani)
    print(verse.translation)

    # Get verse with specific translation
    verse = quran.get_verse(1, 1, translation="en.sahih")

    # Get verse with tafsir
    verse = quran.get_verse(2, 255, include_tafsir=True, tafsir_id=1)
    print(verse.tafsir)

    # Get a range of verses
    verses = quran.get_verses(2, 1, 5)  # Al-Baqarah 1-5
    for v in verses:
        print(f"[{v.ayah}] {v.arabic_uthmani}")

    # Get a random verse
    random_verse = quran.get_random_verse()
    print(f"Random verse: {random_verse.reference}")
```

### Getting Surahs

```python
from quran_unified import QuranAPI

with QuranAPI() as quran:
    # Get surah info only (no verses)
    surah = quran.get_surah_info(1)
    print(f"Name: {surah.name_english}")
    print(f"Arabic: {surah.name_arabic}")
    print(f"Verses: {surah.verses_count}")
    print(f"Revelation: {surah.revelation_type.value}")
    print(f"Order: {surah.revelation_order}")
    print(f"Pages: {surah.pages[0]}-{surah.pages[1]}")

    # Get surah with all verses
    surah = quran.get_surah(1, include_verses=True)
    for verse in surah.verses:
        print(verse.arabic_uthmani)

    # Get all 114 surahs (metadata only)
    all_surahs = quran.get_all_surahs()
    for s in all_surahs:
        print(f"{s.number}. {s.name_english} ({s.verses_count} verses)")
```

### Quran Divisions (Juz, Hizb, Page)

```python
from quran_unified import QuranAPI

with QuranAPI() as quran:
    # Get all verses in Juz 1
    juz_verses = quran.get_juz(1)
    print(f"Juz 1 has {len(juz_verses)} verses")

    # Get all verses in Hizb 1
    hizb_verses = quran.get_hizb(1)

    # Get all verses on Page 1 of the Madani Mushaf
    page_verses = quran.get_page(1)
    for v in page_verses:
        print(f"[{v.reference}] {v.arabic_uthmani}")
```

### Audio Recitations

```python
from quran_unified import QuranAPI

with QuranAPI() as quran:
    # Get audio URL for a single verse
    audio_url = quran.get_audio_url(1, 1, reciter="alafasy")
    print(audio_url)
    # Output: https://everyayah.com/data/Alafasy_128kbps/001001.mp3

    # Get audio URLs for entire surah
    urls = quran.get_surah_audio_urls(1, reciter="alafasy")
    for i, url in enumerate(urls, 1):
        print(f"Verse {i}: {url}")

    # List available reciters
    reciters = quran.get_available_reciters()
    for r in reciters:
        print(f"{r.id}: {r.name_english} ({r.style.value})")
```

#### Available Reciters

| ID | Reciter | Style |
|----|---------|-------|
| `alafasy` | Mishary Rashid Alafasy | Murattal |
| `husary` | Mahmoud Khalil Al-Husary | Murattal |
| `husary_muallim` | Mahmoud Khalil Al-Husary | Muallim |
| `minshawi` | Muhammad Siddiq Al-Minshawi | Mujawwad |
| `sudais` | Abdur-Rahman As-Sudais | Murattal |
| `abdulbasit` | Abdul Basit Abdul Samad | Mujawwad |
| `ghamdi` | Saad Al-Ghamdi | Murattal |
| `shuraym` | Saud Ash-Shuraym | Murattal |
| `ajamy` | Ahmad Al-Ajamy | Murattal |
| `hudhaify` | Ali Al-Hudhaify | Murattal |
| ... | And 30+ more | ... |

### Tafsir (Commentary)

```python
from quran_unified import QuranAPI

with QuranAPI() as quran:
    # Get tafsir for a verse
    tafsir = quran.get_tafsir(2, 255, tafsir_id=1)
    print(f"Tafsir: {tafsir.name}")
    print(f"Author: {tafsir.author}")
    print(f"Text: {tafsir.text}")

    # Get tafsir for a range of verses
    tafsirs = quran.get_tafsir_range(1, 1, 7, tafsir_id=1)
    for t in tafsirs:
        print(t.text)

    # List available tafsirs
    available = quran.get_available_tafsirs()
    for t in available:
        print(f"{t.id}: {t.name} by {t.author}")
```

### Search

```python
from quran_unified import QuranAPI

with QuranAPI() as quran:
    # Search in English
    results = quran.search("mercy", language="en", limit=10)
    for v in results:
        print(f"[{v.reference}] {v.translation}")

    # Search in Arabic
    results = quran.search("الرحمن", language="ar", limit=10)
    for v in results:
        print(f"[{v.reference}] {v.arabic_uthmani}")

    # Search within a specific surah
    results = quran.search("Allah", language="en", surah=2, limit=20)
```

### Translations

```python
from quran_unified import QuranAPI

with QuranAPI() as quran:
    # List all available translations
    translations = quran.get_available_translations()
    for t in translations[:10]:
        print(f"{t.get('identifier', t.get('id'))}: {t.get('name', t.get('englishName'))}")

    # List translations for a specific language
    arabic_trans = quran.get_available_translations(language="ar")
    urdu_trans = quran.get_available_translations(language="ur")
```

## Command Line Interface

The package includes a CLI tool for quick access from the terminal.

### Basic Commands

```bash
# Get a verse
quran verse 2:255
quran verse 1:1 --translation en.sahih

# Get a verse with JSON output
quran verse 2:255 --json

# Get verse with tafsir
quran verse 2:255 --tafsir

# Get surah info
quran surah 1 --info-only

# Get full surah with verses
quran surah 1

# Search the Quran
quran search "mercy" --language en --limit 10
quran search "الرحمن" --language ar

# Get tafsir
quran tafsir 2:255 --tafsir-id 1

# Get audio URL
quran audio 1:1 --reciter alafasy

# List reciters
quran reciters

# List translations
quran translations
quran translations --language ar

# List tafsirs
quran tafsirs
```

### CLI Examples

```bash
# Get Al-Fatihah with translation
$ quran surah 1

الفاتحة - The Opening (Al-Fatihah)
Verses: 7 | Meccan | Order: 5
Pages: 1-1

[1] بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ
    In the name of Allah, the Entirely Merciful, the Especially Merciful.

[2] الْحَمْدُ لِلَّهِ رَبِّ الْعَالَمِينَ
    [All] praise is [due] to Allah, Lord of the worlds -
...

# Get audio URL
$ quran audio 1:1 --reciter alafasy
https://everyayah.com/data/Alafasy_128kbps/001001.mp3

# Search
$ quran search "paradise" --limit 3

Found 3 results for 'paradise':

[2:25] وَبَشِّرِ الَّذِينَ آمَنُوا...
    And give good tidings to those who believe...
...
```

## Configuration

### QuranAPI Options

```python
from quran_unified import QuranAPI

quran = QuranAPI(
    # Default translation for verses
    default_translation="en.sahih",

    # Default reciter for audio
    default_reciter="alafasy",

    # Default tafsir ID
    default_tafsir=1,

    # Cache backend: "memory", "sqlite", or "none"
    cache_backend="memory",

    # Cache time-to-live in seconds (default: 1 hour)
    cache_ttl=3600,

    # Request timeout in seconds
    timeout=30,

    # Number of retry attempts for failed requests
    retries=3,
)
```

### Cache Options

```python
# In-memory cache (default) - fast but not persistent
quran = QuranAPI(cache_backend="memory")

# SQLite cache - persistent across sessions
# Stored at ~/.quran_unified/cache.db
quran = QuranAPI(cache_backend="sqlite")

# No caching - always fetch fresh data
quran = QuranAPI(cache_backend="none")

# Clear cache manually
quran.clear_cache()
```

## Data Sources

This package aggregates data from multiple trusted sources:

| Source | URL | Data Provided |
|--------|-----|---------------|
| **AlQuran Cloud** | api.alquran.cloud | Arabic text, translations, editions |
| **Quran.com** | api.quran.com | Rich metadata, search, translations |
| **QuranEnc** | quranenc.com | Translations with footnotes (by islamiccontent.org) |
| **Tafseer API** | api.quran-tafseer.com | Arabic tafsir commentaries |
| **EveryAyah** | everyayah.com | Audio recitations (44+ reciters) |

## API Reference

### Models

#### Verse
```python
@dataclass
class Verse:
    surah: int              # Surah number (1-114)
    ayah: int               # Ayah number
    arabic_uthmani: str     # Uthmani script text
    arabic_simple: str      # Simple/Imlaei script
    arabic_tajweed: str     # Tajweed markers (if available)
    translation: str        # Translation text
    transliteration: str    # Transliteration
    audio_url: str          # Audio URL
    audio_urls: Dict        # Multiple reciter URLs
    tafsir: str             # Tafsir text
    word_by_word: List      # Word-by-word breakdown
    juz: int                # Juz number (1-30)
    hizb: int               # Hizb number (1-60)
    hizb_quarter: int       # Hizb quarter (1-240)
    ruku: int               # Ruku number
    manzil: int             # Manzil number (1-7)
    page: int               # Madani mushaf page (1-604)
    sajda: bool             # Has sajda
    sajda_type: str         # "recommended" or "obligatory"

    @property
    def reference(self) -> str:  # Returns "surah:ayah"

    def to_dict(self) -> Dict
    def to_json(self) -> str

    @classmethod
    def from_dict(cls, data: Dict) -> Verse
```

#### Surah
```python
@dataclass
class Surah:
    number: int                    # Surah number (1-114)
    name_arabic: str               # Arabic name
    name_english: str              # English name
    name_transliteration: str      # Transliterated name
    verses_count: int              # Number of verses
    revelation_type: RevelationType  # MECCAN or MEDINAN
    revelation_order: int          # Order of revelation
    pages: Tuple[int, int]         # Start and end pages
    verses: List[Verse]            # Loaded verses (optional)

    def to_dict(self) -> Dict

    @classmethod
    def from_dict(cls, data: Dict) -> Surah
```

#### Tafsir
```python
@dataclass
class Tafsir:
    id: int           # Tafsir ID
    name: str         # Tafsir name
    author: str       # Author name
    language: str     # Language code
    book_name: str    # Book name
    text: str         # Tafsir text

    def to_dict(self) -> Dict
```

#### Reciter
```python
@dataclass
class Reciter:
    id: str                    # Reciter identifier
    name_arabic: str           # Arabic name
    name_english: str          # English name
    style: RecitationStyle     # MURATTAL, MUJAWWAD, or MUALLIM
    bitrate: int               # Audio bitrate

    def to_dict(self) -> Dict
```

### QuranAPI Methods

| Method | Description | Returns |
|--------|-------------|---------|
| `get_verse(surah, ayah, ...)` | Get a single verse | `Verse` |
| `get_verses(surah, from_ayah, to_ayah, ...)` | Get verse range | `List[Verse]` |
| `get_random_verse(translation)` | Get random verse | `Verse` |
| `get_surah(surah, ...)` | Get surah with verses | `Surah` |
| `get_surah_info(surah)` | Get surah metadata | `Surah` |
| `get_all_surahs()` | Get all 114 surahs | `List[Surah]` |
| `get_juz(juz, translation)` | Get verses in juz | `List[Verse]` |
| `get_hizb(hizb, translation)` | Get verses in hizb | `List[Verse]` |
| `get_page(page, translation)` | Get verses on page | `List[Verse]` |
| `get_tafsir(surah, ayah, tafsir_id)` | Get tafsir | `Tafsir` |
| `get_tafsir_range(surah, from_ayah, to_ayah, tafsir_id)` | Get tafsir range | `List[Tafsir]` |
| `get_available_tafsirs()` | List tafsirs | `List[Tafsir]` |
| `get_audio_url(surah, ayah, reciter)` | Get audio URL | `str` |
| `get_surah_audio_urls(surah, reciter)` | Get surah audio | `List[str]` |
| `get_available_reciters()` | List reciters | `List[Reciter]` |
| `search(query, language, surah, limit)` | Search Quran | `List[Verse]` |
| `get_available_translations(language)` | List translations | `List[Dict]` |
| `get_verse_count(surah)` | Get verse count | `int` |
| `clear_cache()` | Clear cached data | `None` |
| `close()` | Close connections | `None` |

### Exceptions

```python
from quran_unified import (
    QuranAPIError,          # Base exception
    InvalidReferenceError,  # Invalid surah/ayah
    APIConnectionError,     # Network error
    RateLimitError,         # Rate limit exceeded
    NotFoundError,          # Resource not found
    CacheError,             # Cache operation failed
)

try:
    verse = quran.get_verse(999, 1)  # Invalid surah
except InvalidReferenceError as e:
    print(f"Invalid reference: {e}")
except QuranAPIError as e:
    print(f"API error: {e}")
```

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Development Setup

```bash
# Clone the repository
git clone https://github.com/rwadalebsar/quran-unified.git
cd quran-unified

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run linting
ruff check src/ tests/
mypy src/quran_unified
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [AlQuran Cloud](https://alquran.cloud/) for their comprehensive Quran API
- [Quran.com](https://quran.com/) for rich Quran data and search
- [QuranEnc](https://quranenc.com/) by Islamic Content organization for translations
- [EveryAyah](https://everyayah.com/) for audio recitations
- [Tafseer API](http://api.quran-tafseer.com/) for tafsir data

---

**Made with love for the Muslim Ummah**
