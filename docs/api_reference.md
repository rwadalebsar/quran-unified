# API Reference

Complete reference documentation for the `quran-unified` package.

## QuranAPI Class

The main entry point for accessing Quran data.

### Constructor

```python
QuranAPI(
    default_translation: str = "en.sahih",
    default_reciter: str = "alafasy",
    default_tafsir: int = 1,
    cache_backend: str = "memory",
    cache_ttl: int = 3600,
    timeout: int = 30,
    retries: int = 3,
)
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `default_translation` | str | `"en.sahih"` | Default translation ID |
| `default_reciter` | str | `"alafasy"` | Default reciter ID |
| `default_tafsir` | int | `1` | Default tafsir ID |
| `cache_backend` | str | `"memory"` | Cache type: `"memory"`, `"sqlite"`, or `"none"` |
| `cache_ttl` | int | `3600` | Cache time-to-live in seconds |
| `timeout` | int | `30` | HTTP request timeout in seconds |
| `retries` | int | `3` | Number of retry attempts |

### Context Manager

```python
with QuranAPI() as quran:
    verse = quran.get_verse(1, 1)
# Connection automatically closed
```

---

## Verse Methods

### get_verse()

Get a single verse with optional translation, audio, and tafsir.

```python
get_verse(
    surah: int,
    ayah: int,
    translation: str = None,
    reciter: str = None,
    include_tafsir: bool = False,
    tafsir_id: int = None,
    include_word_by_word: bool = False,
) -> Verse
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `surah` | int | required | Surah number (1-114) |
| `ayah` | int | required | Ayah number |
| `translation` | str | None | Translation ID (uses default if None) |
| `reciter` | str | None | Reciter ID (uses default if None) |
| `include_tafsir` | bool | False | Include tafsir text |
| `tafsir_id` | int | None | Tafsir ID (uses default if None) |
| `include_word_by_word` | bool | False | Include word-by-word breakdown |

**Returns:** `Verse` object

**Example:**
```python
verse = quran.get_verse(2, 255, include_tafsir=True)
print(verse.arabic_uthmani)
print(verse.translation)
print(verse.tafsir)
```

---

### get_verses()

Get a range of verses from a surah.

```python
get_verses(
    surah: int,
    from_ayah: int,
    to_ayah: int,
    translation: str = None,
    reciter: str = None,
) -> List[Verse]
```

**Example:**
```python
verses = quran.get_verses(2, 1, 5)
for v in verses:
    print(f"[{v.ayah}] {v.arabic_uthmani}")
```

---

### get_random_verse()

Get a random verse from the Quran.

```python
get_random_verse(translation: str = None) -> Verse
```

**Example:**
```python
verse = quran.get_random_verse()
print(f"[{verse.reference}] {verse.arabic_uthmani}")
```

---

## Surah Methods

### get_surah()

Get a surah with optional verses.

```python
get_surah(
    surah: int,
    translation: str = None,
    reciter: str = None,
    include_verses: bool = True,
) -> Surah
```

**Example:**
```python
surah = quran.get_surah(1)
print(f"{surah.name_english}: {len(surah.verses)} verses")
```

---

### get_surah_info()

Get surah metadata without verses (faster).

```python
get_surah_info(surah: int) -> Surah
```

**Example:**
```python
surah = quran.get_surah_info(2)
print(f"{surah.name_english}: {surah.verses_count} verses")
```

---

### get_all_surahs()

Get metadata for all 114 surahs.

```python
get_all_surahs() -> List[Surah]
```

**Example:**
```python
surahs = quran.get_all_surahs()
for s in surahs:
    print(f"{s.number}. {s.name_english}")
```

---

## Division Methods

### get_juz()

Get all verses in a juz (1-30).

```python
get_juz(juz: int, translation: str = None) -> List[Verse]
```

---

### get_hizb()

Get all verses in a hizb (1-60).

```python
get_hizb(hizb: int, translation: str = None) -> List[Verse]
```

---

### get_page()

Get all verses on a mushaf page (1-604).

```python
get_page(page: int, translation: str = None) -> List[Verse]
```

---

## Tafsir Methods

### get_tafsir()

Get tafsir for a specific verse.

```python
get_tafsir(
    surah: int,
    ayah: int,
    tafsir_id: int = None,
) -> Tafsir
```

---

### get_tafsir_range()

Get tafsir for a range of verses.

```python
get_tafsir_range(
    surah: int,
    from_ayah: int,
    to_ayah: int,
    tafsir_id: int = None,
) -> List[Tafsir]
```

---

### get_available_tafsirs()

Get list of available tafsirs.

```python
get_available_tafsirs() -> List[Tafsir]
```

---

## Audio Methods

### get_audio_url()

Get audio URL for a specific verse.

```python
get_audio_url(
    surah: int,
    ayah: int,
    reciter: str = None,
) -> str
```

---

### get_surah_audio_urls()

Get audio URLs for all verses in a surah.

```python
get_surah_audio_urls(
    surah: int,
    reciter: str = None,
) -> List[str]
```

---

### get_available_reciters()

Get list of available reciters.

```python
get_available_reciters() -> List[Reciter]
```

---

## Search Methods

### search()

Search the Quran for text.

```python
search(
    query: str,
    language: str = "en",
    surah: int = None,
    limit: int = 50,
) -> List[Verse]
```

---

## Translation Methods

### get_available_translations()

Get list of available translations.

```python
get_available_translations(language: str = None) -> List[Dict]
```

---

## Utility Methods

### get_verse_count()

Get the number of verses in a surah.

```python
get_verse_count(surah: int) -> int
```

---

### clear_cache()

Clear all cached data.

```python
clear_cache() -> None
```

---

### close()

Close all client connections.

```python
close() -> None
```

---

## Data Models

### Verse

```python
@dataclass
class Verse:
    surah: int
    ayah: int
    arabic_uthmani: str
    arabic_simple: str = ""
    arabic_tajweed: str = ""
    translation: str = ""
    transliteration: str = ""
    audio_url: str = ""
    audio_urls: Dict[str, str] = field(default_factory=dict)
    tafsir: str = ""
    word_by_word: List[Dict] = field(default_factory=list)
    juz: int = 0
    hizb: int = 0
    hizb_quarter: int = 0
    ruku: int = 0
    manzil: int = 0
    page: int = 0
    sajda: bool = False
    sajda_type: str = ""

    @property
    def reference(self) -> str

    @property
    def verse_key(self) -> str

    def to_dict(self) -> Dict
    def to_json(self) -> str

    @classmethod
    def from_dict(cls, data: Dict) -> Verse
```

### Surah

```python
@dataclass
class Surah:
    number: int
    name_arabic: str
    name_english: str
    name_transliteration: str
    verses_count: int
    revelation_type: RevelationType
    revelation_order: int
    pages: Tuple[int, int] = (0, 0)
    verses: List[Verse] = field(default_factory=list)

    def to_dict(self) -> Dict

    @classmethod
    def from_dict(cls, data: Dict) -> Surah
```

### Tafsir

```python
@dataclass
class Tafsir:
    id: int
    name: str
    author: str
    language: str
    book_name: str = ""
    text: str = ""

    def to_dict(self) -> Dict

    @classmethod
    def from_dict(cls, data: Dict) -> Tafsir
```

### Reciter

```python
@dataclass
class Reciter:
    id: str
    name_arabic: str
    name_english: str
    style: RecitationStyle
    bitrate: int = 128

    def to_dict(self) -> Dict

    @classmethod
    def from_dict(cls, data: Dict) -> Reciter
```

### Enums

```python
class RevelationType(Enum):
    MECCAN = "Meccan"
    MEDINAN = "Medinan"

class RecitationStyle(Enum):
    MURATTAL = "Murattal"
    MUJAWWAD = "Mujawwad"
    MUALLIM = "Muallim"
```

---

## Exceptions

```python
class QuranAPIError(Exception):
    """Base exception for all Quran API errors."""

class InvalidReferenceError(QuranAPIError):
    """Raised when an invalid surah/ayah reference is provided."""

class APIConnectionError(QuranAPIError):
    """Raised when connection to the API fails."""

class RateLimitError(QuranAPIError):
    """Raised when API rate limit is exceeded."""

class NotFoundError(QuranAPIError):
    """Raised when requested resource is not found."""

class CacheError(QuranAPIError):
    """Raised when a cache operation fails."""
```

**Usage:**
```python
from quran_unified import QuranAPI, InvalidReferenceError, QuranAPIError

try:
    verse = quran.get_verse(999, 1)
except InvalidReferenceError as e:
    print(f"Invalid reference: {e}")
except QuranAPIError as e:
    print(f"API error: {e}")
```
