"""Client for the QuranEnc API (https://quranenc.com), operated by islamiccontent.org."""

from typing import Any, Dict, List, Optional

from quran_unified.clients.base import BaseClient


class QuranEncClient(BaseClient):
    """Client for QuranEnc.com — Encyclopedia of Quran translations.

    Operated by islamiccontent.org (جمعية خدمة المحتوى الإسلامي باللغات).
    Provides translations with footnotes in many languages.
    """

    BASE_URL = "https://quranenc.com/api/v1"

    def get_translations_list(
        self, language: Optional[str] = None, localization: str = "en"
    ) -> List[Dict[str, Any]]:
        """List available translations, optionally filtered by language.

        Args:
            language: ISO language code to filter by (e.g. "en", "ar", "es").
            localization: Locale for title/description fields. Defaults to "en".

        Returns:
            List of dicts with keys: key, language_iso_code, version,
            last_update, title, description.
        """
        endpoint = "/translations/list"
        if language:
            endpoint += f"/{language}"
        params: Dict[str, str] = {}
        if localization != "en":
            params["localization"] = localization
        return self._get(endpoint, params=params or None)

    def get_sura_translation(
        self, translation_key: str, sura: int
    ) -> List[Dict[str, Any]]:
        """Get translation for an entire surah.

        Args:
            translation_key: Translation identifier (e.g. "english_saheeh").
            sura: Surah number (1-114).

        Returns:
            List of dicts with keys: sura, aya, translation, footnotes.
        """
        return self._get(f"/translation/sura/{translation_key}/{sura}")

    def get_aya_translation(
        self, translation_key: str, sura: int, aya: int
    ) -> Dict[str, Any]:
        """Get translation for a single ayah.

        Args:
            translation_key: Translation identifier (e.g. "english_saheeh").
            sura: Surah number (1-114).
            aya: Ayah number within the surah.

        Returns:
            Dict with keys: sura, aya, translation, footnotes.
        """
        return self._get(f"/translation/aya/{translation_key}/{sura}/{aya}")
