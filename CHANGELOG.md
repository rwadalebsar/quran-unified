# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2025-01-28

### Added

- Initial release of `quran-unified`
- **QuranAPI** - Unified interface for accessing Quran data
- **Data Models**
  - `Verse` - Represents a single Quran verse with text, translation, audio, and metadata
  - `Surah` - Represents a Quran chapter with metadata
  - `Tafsir` - Represents tafsir/commentary
  - `Reciter` - Represents a Quran reciter
- **API Clients**
  - `AlQuranCloudClient` - Client for AlQuran Cloud API
  - `QuranComClient` - Client for Quran.com API
  - `QuranEncClient` - Client for QuranEnc.com API (islamiccontent.org)
  - `TafseerAPIClient` - Client for Tafseer API
  - `EveryAyahClient` - Client for EveryAyah audio URLs
- **Cache Backends**
  - `MemoryCache` - In-memory LRU cache
  - `SQLiteCache` - Persistent SQLite cache
  - `NoCache` - Disabled caching option
- **CLI Tool**
  - `quran verse` - Get verse by reference
  - `quran surah` - Get surah by number
  - `quran search` - Search the Quran
  - `quran tafsir` - Get tafsir for a verse
  - `quran audio` - Get audio URL
  - `quran reciters` - List available reciters
  - `quran translations` - List available translations
  - `quran tafsirs` - List available tafsirs
- **Features**
  - Multiple Arabic text scripts (Uthmani, Simple, Tajweed)
  - 100+ translations in 40+ languages
  - Audio recitations from 44+ reciters
  - Quran divisions (Juz, Hizb, Page)
  - Smart caching with configurable TTL
  - Context manager support
  - Full type hints

### Data Sources

- AlQuran Cloud (api.alquran.cloud)
- Quran.com (api.quran.com)
- QuranEnc (quranenc.com)
- Tafseer API (api.quran-tafseer.com)
- EveryAyah (everyayah.com)

---

## Future Releases

### Planned Features

- Async support with `aiohttp`
- Word-by-word translation and transliteration
- Additional tafsir sources
- Tajweed color-coded text
- Bookmark/favorites system
- Offline mode with local data

---

[0.1.0]: https://github.com/rwadalebsar/quran-unified/releases/tag/v0.1.0
