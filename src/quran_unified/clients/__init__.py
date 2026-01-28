"""API clients for various Quran data sources."""

from quran_unified.clients.alquran_cloud import AlQuranCloudClient
from quran_unified.clients.base import BaseClient
from quran_unified.clients.everyayah import EveryAyahClient
from quran_unified.clients.quran_com import QuranComClient
from quran_unified.clients.quranenc import QuranEncClient
from quran_unified.clients.tafseer_api import TafseerAPIClient

__all__ = [
    "BaseClient",
    "AlQuranCloudClient",
    "QuranComClient",
    "TafseerAPIClient",
    "EveryAyahClient",
    "QuranEncClient",
]
