"""Client for the Tafseer API (http://api.quran-tafseer.com)."""

from typing import Any, Dict, List

from quran_unified.clients.base import BaseClient


class TafseerAPIClient(BaseClient):
    """Client for the Tafseer API. Provides Arabic tafsirs."""

    BASE_URL = "http://api.quran-tafseer.com"

    def get_tafsirs(self) -> List[Dict[str, Any]]:
        """List all available tafsirs."""
        return self._get("/tafseer")

    def get_tafsir(self, tafsir_id: int, surah: int, ayah: int) -> Dict[str, Any]:
        """Get tafsir for a single ayah."""
        return self._get(f"/tafseer/{tafsir_id}/{surah}/{ayah}")

    def get_tafsir_range(
        self, tafsir_id: int, surah: int, from_ayah: int, to_ayah: int
    ) -> List[Dict[str, Any]]:
        """Get tafsir for a range of ayahs in a surah."""
        return self._get(f"/tafseer/{tafsir_id}/{surah}/{from_ayah}/{to_ayah}")

    def get_quran_text(self, surah: int, ayah: int) -> Dict[str, Any]:
        """Get Quran text for a specific ayah."""
        return self._get(f"/quran/{surah}/{ayah}")
