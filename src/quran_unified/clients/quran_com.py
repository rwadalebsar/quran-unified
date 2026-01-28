"""Client for the Quran.com API v4 (https://api.quran.com/api/v4)."""

from typing import Any, Dict, List, Optional

from quran_unified.clients.base import BaseClient


class QuranComClient(BaseClient):
    """Client for Quran.com API. Rich metadata and best search capabilities."""

    BASE_URL = "https://api.quran.com/api/v4"

    def get_verse(
        self,
        surah: int,
        ayah: int,
        translations: Optional[str] = None,
        fields: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Get a single verse by surah and ayah."""
        params: Dict[str, Any] = {}
        if translations:
            params["translations"] = translations
        if fields:
            params["fields"] = fields
        return self._get(f"/verses/by_key/{surah}:{ayah}", params=params or None)

    def get_verses_by_chapter(
        self,
        surah: int,
        translations: Optional[str] = None,
        per_page: int = 50,
    ) -> Dict[str, Any]:
        """Get all verses of a chapter (surah)."""
        params: Dict[str, Any] = {"per_page": per_page}
        if translations:
            params["translations"] = translations
        return self._get(f"/verses/by_chapter/{surah}", params=params)

    def get_verses_by_juz(
        self, juz: int, translations: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get all verses in a juz."""
        params: Dict[str, Any] = {}
        if translations:
            params["translations"] = translations
        return self._get(f"/verses/by_juz/{juz}", params=params or None)

    def get_verses_by_page(
        self, page: int, translations: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get all verses on a mushaf page."""
        params: Dict[str, Any] = {}
        if translations:
            params["translations"] = translations
        return self._get(f"/verses/by_page/{page}", params=params or None)

    def get_chapter(self, surah: int) -> Dict[str, Any]:
        """Get chapter (surah) metadata."""
        return self._get(f"/chapters/{surah}")

    def get_chapters(self) -> List[Dict[str, Any]]:
        """Get metadata for all chapters."""
        data = self._get("/chapters")
        return data.get("chapters", data)

    def get_translations(self, language: str = "en") -> List[Dict[str, Any]]:
        """List available translations for a language."""
        data = self._get("/resources/translations", params={"language": language})
        return data.get("translations", data)

    def get_tafsirs(self, language: str = "en") -> List[Dict[str, Any]]:
        """List available tafsirs for a language."""
        data = self._get("/resources/tafsirs", params={"language": language})
        return data.get("tafsirs", data)

    def get_reciters(self) -> List[Dict[str, Any]]:
        """List available reciters."""
        data = self._get("/resources/recitations")
        return data.get("recitations", data)

    def search(
        self, query: str, language: str = "en", page: int = 1
    ) -> Dict[str, Any]:
        """Search the Quran."""
        return self._get(
            "/search", params={"q": query, "language": language, "page": page}
        )
