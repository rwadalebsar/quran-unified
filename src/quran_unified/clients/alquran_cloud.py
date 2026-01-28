"""Client for the AlQuran Cloud API (https://alquran.cloud/api)."""

from typing import Any, Dict, List, Optional

from quran_unified.clients.base import BaseClient
from quran_unified.exceptions import QuranAPIError


class AlQuranCloudClient(BaseClient):
    """Client for AlQuran Cloud API. No rate limits. Multiple editions support."""

    BASE_URL = "https://api.alquran.cloud/v1"

    def _parse_response(self, data: Dict[str, Any]) -> Any:
        """Extract data from the AlQuran Cloud response envelope."""
        if data.get("code") != 200 or data.get("status") != "OK":
            raise QuranAPIError(
                f"AlQuran Cloud API error: {data.get('status', 'Unknown')}"
            )
        return data["data"]

    def get_verse(self, surah: int, ayah: int, edition: str = "quran-uthmani") -> Dict[str, Any]:
        """Get a single verse by surah and ayah number."""
        data = self._get(f"/ayah/{surah}:{ayah}/{edition}")
        return self._parse_response(data)

    def get_verse_multi(
        self, surah: int, ayah: int, editions: List[str]
    ) -> List[Dict[str, Any]]:
        """Get a verse from multiple editions at once."""
        editions_str = ",".join(editions)
        data = self._get(f"/ayah/{surah}:{ayah}/editions/{editions_str}")
        return self._parse_response(data)

    def get_surah(self, surah: int, edition: str = "quran-uthmani") -> Dict[str, Any]:
        """Get all verses of a surah."""
        data = self._get(f"/surah/{surah}/{edition}")
        return self._parse_response(data)

    def get_juz(self, juz: int, edition: str = "quran-uthmani") -> Dict[str, Any]:
        """Get all verses in a juz."""
        data = self._get(f"/juz/{juz}/{edition}")
        return self._parse_response(data)

    def get_page(self, page: int, edition: str = "quran-uthmani") -> Dict[str, Any]:
        """Get all verses on a mushaf page."""
        data = self._get(f"/page/{page}/{edition}")
        return self._parse_response(data)

    def get_editions(
        self,
        format: Optional[str] = None,
        language: Optional[str] = None,
        type: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """List available editions with optional filters."""
        params = {}
        if format:
            params["format"] = format
        if language:
            params["language"] = language
        if type:
            params["type"] = type
        data = self._get("/edition", params=params or None)
        return self._parse_response(data)

    def search(
        self, query: str, edition: str = "en.sahih", surah: Optional[int] = None
    ) -> Dict[str, Any]:
        """Search for text across the Quran."""
        endpoint = f"/search/{query}/{edition}"
        if surah is not None:
            endpoint += f"/{surah}"
        data = self._get(endpoint)
        return self._parse_response(data)
