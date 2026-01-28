"""Pytest fixtures and configuration."""

import pytest

from quran_unified import QuranAPI
from quran_unified.cache import MemoryCache, NoCache
from quran_unified.models import Reciter, RecitationStyle, RevelationType, Surah, Tafsir, Verse


@pytest.fixture
def quran_api():
    """Create a QuranAPI instance with caching disabled."""
    api = QuranAPI(cache_backend="none")
    yield api
    api.close()


@pytest.fixture
def memory_cache():
    """Create a memory cache instance."""
    return MemoryCache(max_size=100)


@pytest.fixture
def no_cache():
    """Create a no-op cache instance."""
    return NoCache()


@pytest.fixture
def sample_verse_data():
    """Sample verse data for testing."""
    return {
        "surah": 1,
        "ayah": 1,
        "arabic_uthmani": "بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ",
        "arabic_simple": "بسم الله الرحمن الرحيم",
        "translation": "In the name of Allah, the Entirely Merciful, the Especially Merciful.",
        "juz": 1,
        "page": 1,
    }


@pytest.fixture
def sample_verse(sample_verse_data):
    """Create a sample Verse instance."""
    return Verse(**sample_verse_data)


@pytest.fixture
def sample_surah_data():
    """Sample surah data for testing."""
    return {
        "number": 1,
        "name_arabic": "الفاتحة",
        "name_english": "The Opening",
        "name_transliteration": "Al-Fatihah",
        "verses_count": 7,
        "revelation_type": RevelationType.MECCAN,
        "revelation_order": 5,
        "pages": (1, 1),
    }


@pytest.fixture
def sample_surah(sample_surah_data):
    """Create a sample Surah instance."""
    return Surah(**sample_surah_data)


@pytest.fixture
def sample_tafsir_data():
    """Sample tafsir data for testing."""
    return {
        "id": 1,
        "name": "Tafsir Ibn Kathir",
        "author": "Ibn Kathir",
        "language": "ar",
        "book_name": "تفسير ابن كثير",
        "text": "Sample tafsir text...",
    }


@pytest.fixture
def sample_tafsir(sample_tafsir_data):
    """Create a sample Tafsir instance."""
    return Tafsir(**sample_tafsir_data)


@pytest.fixture
def sample_reciter_data():
    """Sample reciter data for testing."""
    return {
        "id": "alafasy",
        "name_arabic": "مشاري العفاسي",
        "name_english": "Mishary Rashid Alafasy",
        "style": RecitationStyle.MURATTAL,
        "bitrate": 128,
    }


@pytest.fixture
def sample_reciter(sample_reciter_data):
    """Create a sample Reciter instance."""
    return Reciter(**sample_reciter_data)
