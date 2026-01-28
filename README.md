# Quran Unified

A unified Python wrapper for multiple Quran data sources. Access Quran text, translations, audio, and tafsir through a single, simple API.

## Features

- **Unified API**: Single interface to access data from multiple sources
- **Multiple Data Sources**: AlQuran Cloud, Quran.com, QuranEnc, Tafseer API, EveryAyah
- **Text Variants**: Uthmani, Simple, and Tajweed scripts
- **Translations**: 100+ translations in 40+ languages
- **Audio**: Recitations from 44+ reciters
- **Tafsir**: Arabic tafsir/commentary
- **Caching**: Built-in memory and SQLite caching
- **CLI**: Command-line interface for quick access

## Installation

```bash
pip install quran-unified
```

For development:

```bash
pip install quran-unified[dev]
```

## Quick Start

```python
from quran_unified import QuranAPI

# Create API instance
quran = QuranAPI()

# Get a verse
verse = quran.get_verse(2, 255)  # Ayat al-Kursi
print(verse.arabic_uthmani)
print(verse.translation)
print(verse.audio_url)

# Get surah info
surah = quran.get_surah_info(1)
print(f"{surah.name_english}: {surah.verses_count} verses")

# Search
results = quran.search("mercy", language="en")
for v in results[:5]:
    print(f"[{v.reference}] {v.translation}")

# Get audio URL
audio = quran.get_audio_url(1, 1, reciter="alafasy")
print(audio)

# Clean up
quran.close()
```

### Using Context Manager

```python
from quran_unified import QuranAPI

with QuranAPI() as quran:
    verse = quran.get_verse(1, 1)
    print(verse.arabic_uthmani)
```

## CLI Usage

```bash
# Get a verse
quran verse 2:255
quran verse 2:255 --translation en.sahih --json

# Get surah info
quran surah 1
quran surah 1 --info-only

# Search
quran search "الرحمن"
quran search "mercy" --language en --limit 10

# Get tafsir
quran tafsir 2:255 --tafsir-id 1

# Get audio URL
quran audio 1:1 --reciter alafasy

# List reciters
quran reciters

# List translations
quran translations --language ar
```

## Configuration

```python
quran = QuranAPI(
    default_translation="en.sahih",  # Default translation
    default_reciter="alafasy",       # Default reciter
    default_tafsir=1,                # Default tafsir ID
    cache_backend="memory",          # "memory", "sqlite", or "none"
    cache_ttl=3600,                  # Cache TTL in seconds
    timeout=30,                      # Request timeout
    retries=3,                       # Retry attempts
)
```

## API Reference

### Verse Methods

| Method | Description |
|--------|-------------|
| `get_verse(surah, ayah, ...)` | Get a single verse |
| `get_verses(surah, from_ayah, to_ayah, ...)` | Get a range of verses |
| `get_random_verse(translation)` | Get a random verse |

### Surah Methods

| Method | Description |
|--------|-------------|
| `get_surah(surah, ...)` | Get surah with verses |
| `get_surah_info(surah)` | Get surah metadata only |
| `get_all_surahs()` | Get all 114 surahs |

### Division Methods

| Method | Description |
|--------|-------------|
| `get_juz(juz, translation)` | Get verses in a juz (1-30) |
| `get_hizb(hizb, translation)` | Get verses in a hizb (1-60) |
| `get_page(page, translation)` | Get verses on a page (1-604) |

### Tafsir Methods

| Method | Description |
|--------|-------------|
| `get_tafsir(surah, ayah, tafsir_id)` | Get tafsir for a verse |
| `get_available_tafsirs()` | List available tafsirs |

### Audio Methods

| Method | Description |
|--------|-------------|
| `get_audio_url(surah, ayah, reciter)` | Get audio URL |
| `get_surah_audio_urls(surah, reciter)` | Get all audio URLs for surah |
| `get_available_reciters()` | List available reciters |

### Search & Utility

| Method | Description |
|--------|-------------|
| `search(query, language, surah, limit)` | Search the Quran |
| `get_available_translations(language)` | List translations |
| `get_verse_count(surah)` | Get verse count for surah |
| `clear_cache()` | Clear cached data |

## Data Sources

| Source | URL | Data Provided |
|--------|-----|---------------|
| AlQuran Cloud | api.alquran.cloud | Text, translations, search |
| Quran.com | api.quran.com | Rich metadata, search |
| QuranEnc | quranenc.com | Translations with footnotes |
| Tafseer API | api.quran-tafseer.com | Arabic tafsirs |
| EveryAyah | everyayah.com | Audio recitations |

## License

MIT License - see [LICENSE](LICENSE) for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
