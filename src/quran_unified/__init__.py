"""Unified Python wrapper for multiple Quran data sources."""

from quran_unified.api import QuranAPI
from quran_unified.exceptions import (
    APIConnectionError,
    CacheError,
    InvalidReferenceError,
    NotFoundError,
    QuranAPIError,
    RateLimitError,
)
from quran_unified.models.reciter import Reciter, RecitationStyle
from quran_unified.models.surah import RevelationType, Surah
from quran_unified.models.tafsir import Tafsir
from quran_unified.models.verse import Verse

__version__ = "0.1.0"

__all__ = [
    "QuranAPI",
    "Verse",
    "Surah",
    "Tafsir",
    "Reciter",
    "RevelationType",
    "RecitationStyle",
    "QuranAPIError",
    "InvalidReferenceError",
    "APIConnectionError",
    "RateLimitError",
    "NotFoundError",
    "CacheError",
]
