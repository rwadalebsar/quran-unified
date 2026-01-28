"""Main QuranAPI unified interface."""

import random
from typing import Any, Dict, List, Optional, Union

from quran_unified.cache import MemoryCache, NoCache, SQLiteCache
from quran_unified.cache.base import CacheBackend
from quran_unified.clients.alquran_cloud import AlQuranCloudClient
from quran_unified.clients.everyayah import EveryAyahClient
from quran_unified.clients.quran_com import QuranComClient
from quran_unified.clients.quranenc import QuranEncClient
from quran_unified.clients.tafseer_api import TafseerAPIClient
from quran_unified.exceptions import InvalidReferenceError
from quran_unified.models.reciter import Reciter, RecitationStyle
from quran_unified.models.surah import RevelationType, Surah
from quran_unified.models.tafsir import Tafsir
from quran_unified.models.verse import Verse
from quran_unified.utils.constants import RECITER_INFO, SURAH_DATA, VERSE_COUNTS


class QuranAPI:
    """Unified interface for all Quran data sources.

    Example:
        quran = QuranAPI()
        verse = quran.get_verse(2, 255)
        print(verse.arabic_uthmani)
    """

    def __init__(
        self,
        default_translation: str = "en.sahih",
        default_reciter: str = "alafasy",
        default_tafsir: int = 1,
        cache_backend: str = "memory",
        cache_ttl: int = 3600,
        timeout: int = 30,
        retries: int = 3,
    ):
        self.default_translation = default_translation
        self.default_reciter = default_reciter
        self.default_tafsir = default_tafsir
        self.cache_ttl = cache_ttl

        # Initialize cache
        self._cache: CacheBackend
        if cache_backend == "memory":
            self._cache = MemoryCache()
        elif cache_backend == "sqlite":
            self._cache = SQLiteCache()
        else:
            self._cache = NoCache()

        # Initialize clients
        self._alquran = AlQuranCloudClient(timeout=timeout, retries=retries)
        self._qurancom = QuranComClient(timeout=timeout, retries=retries)
        self._tafseer = TafseerAPIClient(timeout=timeout, retries=retries)
        self._everyayah = EveryAyahClient()
        self._quranenc = QuranEncClient(timeout=timeout, retries=retries)

    # ==================== Verse Methods ====================

    def get_verse(
        self,
        surah: int,
        ayah: int,
        translation: Optional[str] = None,
        reciter: Optional[str] = None,
        include_tafsir: bool = False,
        tafsir_id: Optional[int] = None,
        include_word_by_word: bool = False,
    ) -> Verse:
        """Get a single verse with optional translation, audio, and tafsir."""
        self._validate_reference(surah, ayah)
        translation = translation or self.default_translation
        reciter = reciter or self.default_reciter

        cache_key = f"verse:{surah}:{ayah}:{translation}:{reciter}:{include_tafsir}:{tafsir_id}"
        cached = self._cache.get(cache_key)
        if cached:
            return Verse.from_dict(cached)

        # Get base verse data from AlQuran Cloud
        data = self._alquran.get_verse(surah, ayah, "quran-uthmani")

        verse = Verse(
            surah=surah,
            ayah=ayah,
            arabic_uthmani=data.get("text", ""),
            juz=data.get("juz", 0),
            hizb=data.get("hizbQuarter", 0) // 4 + 1 if data.get("hizbQuarter") else 0,
            hizb_quarter=data.get("hizbQuarter", 0),
            page=data.get("page", 0),
            manzil=data.get("manzil", 0),
            ruku=data.get("ruku", 0),
            sajda=data.get("sajda", False) if isinstance(data.get("sajda"), bool) else bool(data.get("sajda")),
        )

        # Get translation
        if translation:
            try:
                trans_data = self._alquran.get_verse(surah, ayah, translation)
                verse.translation = trans_data.get("text", "")
            except Exception:
                pass

        # Get audio URL
        verse.audio_url = self._everyayah.get_audio_url(surah, ayah, reciter)

        # Get tafsir if requested
        if include_tafsir:
            tid = tafsir_id or self.default_tafsir
            try:
                tafsir_data = self._tafseer.get_tafsir(tid, surah, ayah)
                verse.tafsir = tafsir_data.get("text", "")
            except Exception:
                pass

        self._cache.set(cache_key, verse.to_dict(), self.cache_ttl)
        return verse

    def get_verses(
        self,
        surah: int,
        from_ayah: int,
        to_ayah: int,
        translation: Optional[str] = None,
        reciter: Optional[str] = None,
    ) -> List[Verse]:
        """Get a range of verses from a surah."""
        self._validate_reference(surah, from_ayah)
        self._validate_reference(surah, to_ayah)
        return [
            self.get_verse(surah, ayah, translation, reciter)
            for ayah in range(from_ayah, to_ayah + 1)
        ]

    def get_random_verse(self, translation: Optional[str] = None) -> Verse:
        """Get a random verse from the Quran."""
        surah = random.randint(1, 114)
        max_ayah = VERSE_COUNTS[surah - 1]
        ayah = random.randint(1, max_ayah)
        return self.get_verse(surah, ayah, translation)

    # ==================== Surah Methods ====================

    def get_surah(
        self,
        surah: int,
        translation: Optional[str] = None,
        reciter: Optional[str] = None,
        include_verses: bool = True,
    ) -> Surah:
        """Get a surah with optional verses loaded."""
        self._validate_surah(surah)

        surah_info = self.get_surah_info(surah)

        if include_verses:
            surah_info.verses = [
                self.get_verse(surah, ayah, translation, reciter)
                for ayah in range(1, surah_info.verses_count + 1)
            ]

        return surah_info

    def get_surah_info(self, surah: int) -> Surah:
        """Get surah metadata without verses."""
        self._validate_surah(surah)

        cache_key = f"surah_info:{surah}"
        cached = self._cache.get(cache_key)
        if cached:
            return Surah.from_dict(cached)

        data = SURAH_DATA[surah - 1]
        surah_obj = Surah(
            number=surah,
            name_arabic=data["name_arabic"],
            name_english=data["name_english"],
            name_transliteration=data["name_transliteration"],
            verses_count=data["verses_count"],
            revelation_type=RevelationType(data["revelation_type"]),
            revelation_order=data["revelation_order"],
            pages=data["pages"],
        )

        self._cache.set(cache_key, surah_obj.to_dict(), self.cache_ttl)
        return surah_obj

    def get_all_surahs(self) -> List[Surah]:
        """Get metadata for all 114 surahs."""
        return [self.get_surah_info(i) for i in range(1, 115)]

    # ==================== Juz/Hizb/Page Methods ====================

    def get_juz(self, juz: int, translation: Optional[str] = None) -> List[Verse]:
        """Get all verses in a juz."""
        if not 1 <= juz <= 30:
            raise InvalidReferenceError(f"Invalid juz: {juz}. Must be 1-30.")

        cache_key = f"juz:{juz}:{translation or self.default_translation}"
        cached = self._cache.get(cache_key)
        if cached:
            return [Verse.from_dict(v) for v in cached]

        data = self._alquran.get_juz(juz, translation or self.default_translation)
        verses = []
        for ayah_data in data.get("ayahs", []):
            ref = ayah_data.get("number", 0)
            surah_num = ayah_data.get("surah", {}).get("number", 1)
            ayah_num = ayah_data.get("numberInSurah", 1)
            verses.append(
                Verse(
                    surah=surah_num,
                    ayah=ayah_num,
                    arabic_uthmani=ayah_data.get("text", ""),
                    juz=juz,
                    page=ayah_data.get("page", 0),
                )
            )

        self._cache.set(cache_key, [v.to_dict() for v in verses], self.cache_ttl)
        return verses

    def get_hizb(self, hizb: int, translation: Optional[str] = None) -> List[Verse]:
        """Get all verses in a hizb."""
        if not 1 <= hizb <= 60:
            raise InvalidReferenceError(f"Invalid hizb: {hizb}. Must be 1-60.")

        # Hizb maps to juz (2 hizbs per juz)
        juz = (hizb - 1) // 2 + 1
        all_verses = self.get_juz(juz, translation)

        # Filter to the specific hizb
        target_quarters = [(hizb - 1) * 4 + i for i in range(1, 5)]
        return [v for v in all_verses if v.hizb == hizb or v.hizb_quarter in target_quarters]

    def get_page(self, page: int, translation: Optional[str] = None) -> List[Verse]:
        """Get all verses on a mushaf page."""
        if not 1 <= page <= 604:
            raise InvalidReferenceError(f"Invalid page: {page}. Must be 1-604.")

        cache_key = f"page:{page}:{translation or self.default_translation}"
        cached = self._cache.get(cache_key)
        if cached:
            return [Verse.from_dict(v) for v in cached]

        data = self._alquran.get_page(page, translation or self.default_translation)
        verses = []
        for ayah_data in data.get("ayahs", []):
            surah_num = ayah_data.get("surah", {}).get("number", 1)
            ayah_num = ayah_data.get("numberInSurah", 1)
            verses.append(
                Verse(
                    surah=surah_num,
                    ayah=ayah_num,
                    arabic_uthmani=ayah_data.get("text", ""),
                    page=page,
                )
            )

        self._cache.set(cache_key, [v.to_dict() for v in verses], self.cache_ttl)
        return verses

    # ==================== Tafsir Methods ====================

    def get_tafsir(
        self, surah: int, ayah: int, tafsir_id: Optional[int] = None
    ) -> Tafsir:
        """Get tafsir for a specific verse."""
        self._validate_reference(surah, ayah)
        tid = tafsir_id or self.default_tafsir

        cache_key = f"tafsir:{surah}:{ayah}:{tid}"
        cached = self._cache.get(cache_key)
        if cached:
            return Tafsir.from_dict(cached)

        data = self._tafseer.get_tafsir(tid, surah, ayah)

        # Get tafsir metadata
        tafsirs = self._get_tafsir_list()
        tafsir_meta = next((t for t in tafsirs if t.get("id") == tid), {})

        tafsir = Tafsir(
            id=tid,
            name=tafsir_meta.get("name", ""),
            author=tafsir_meta.get("author", ""),
            language=tafsir_meta.get("language", "ar"),
            book_name=tafsir_meta.get("book_name", ""),
            text=data.get("text", ""),
        )

        self._cache.set(cache_key, tafsir.to_dict(), self.cache_ttl)
        return tafsir

    def get_tafsir_range(
        self,
        surah: int,
        from_ayah: int,
        to_ayah: int,
        tafsir_id: Optional[int] = None,
    ) -> List[Tafsir]:
        """Get tafsir for a range of verses."""
        self._validate_reference(surah, from_ayah)
        self._validate_reference(surah, to_ayah)
        return [
            self.get_tafsir(surah, ayah, tafsir_id)
            for ayah in range(from_ayah, to_ayah + 1)
        ]

    def get_available_tafsirs(self) -> List[Tafsir]:
        """Get list of available tafsirs."""
        tafsirs = self._get_tafsir_list()
        return [
            Tafsir(
                id=t.get("id", 0),
                name=t.get("name", ""),
                author=t.get("author", ""),
                language=t.get("language", "ar"),
                book_name=t.get("book_name", ""),
            )
            for t in tafsirs
        ]

    def _get_tafsir_list(self) -> List[Dict[str, Any]]:
        """Get cached tafsir list."""
        cache_key = "tafsir_list"
        cached = self._cache.get(cache_key)
        if cached:
            return cached

        tafsirs = self._tafseer.get_tafsirs()
        self._cache.set(cache_key, tafsirs, self.cache_ttl * 24)
        return tafsirs

    # ==================== Audio Methods ====================

    def get_audio_url(
        self, surah: int, ayah: int, reciter: Optional[str] = None
    ) -> str:
        """Get audio URL for a specific verse."""
        self._validate_reference(surah, ayah)
        return self._everyayah.get_audio_url(surah, ayah, reciter or self.default_reciter)

    def get_surah_audio_urls(
        self, surah: int, reciter: Optional[str] = None
    ) -> List[str]:
        """Get audio URLs for all verses in a surah."""
        self._validate_surah(surah)
        total = VERSE_COUNTS[surah - 1]
        return self._everyayah.get_surah_audio_urls(
            surah, total, reciter or self.default_reciter
        )

    def get_available_reciters(self) -> List[Reciter]:
        """Get list of available reciters."""
        reciters = []
        for rid, info in RECITER_INFO.items():
            reciters.append(
                Reciter(
                    id=rid,
                    name_arabic=info["name_arabic"],
                    name_english=info["name_english"],
                    style=RecitationStyle(info["style"]),
                    bitrate=info.get("bitrate", 128),
                )
            )
        return reciters

    # ==================== Search Methods ====================

    def search(
        self,
        query: str,
        language: str = "en",
        surah: Optional[int] = None,
        limit: int = 50,
    ) -> List[Verse]:
        """Search the Quran for text."""
        cache_key = f"search:{query}:{language}:{surah}:{limit}"
        cached = self._cache.get(cache_key)
        if cached:
            return [Verse.from_dict(v) for v in cached]

        # Use Quran.com for better search
        data = self._qurancom.search(query, language)
        results = data.get("search", {}).get("results", [])

        verses = []
        for r in results[:limit]:
            verse_key = r.get("verse_key", "1:1")
            parts = verse_key.split(":")
            s, a = int(parts[0]), int(parts[1])
            if surah and s != surah:
                continue
            verses.append(
                Verse(
                    surah=s,
                    ayah=a,
                    arabic_uthmani=r.get("text", ""),
                    translation=r.get("translations", [{}])[0].get("text", "") if r.get("translations") else "",
                )
            )

        self._cache.set(cache_key, [v.to_dict() for v in verses], self.cache_ttl)
        return verses

    # ==================== Translation Methods ====================

    def get_available_translations(
        self, language: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Get list of available translations."""
        cache_key = f"translations:{language or 'all'}"
        cached = self._cache.get(cache_key)
        if cached:
            return cached

        if language:
            translations = self._qurancom.get_translations(language)
        else:
            translations = self._alquran.get_editions(type="translation")

        self._cache.set(cache_key, translations, self.cache_ttl * 24)
        return translations

    # ==================== Utility Methods ====================

    def get_verse_count(self, surah: int) -> int:
        """Get the number of verses in a surah."""
        self._validate_surah(surah)
        return VERSE_COUNTS[surah - 1]

    def clear_cache(self) -> None:
        """Clear all cached data."""
        self._cache.clear()

    def close(self) -> None:
        """Close all client connections."""
        self._alquran.close()
        self._qurancom.close()
        self._tafseer.close()
        self._quranenc.close()

    def __enter__(self) -> "QuranAPI":
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()

    # ==================== Validation ====================

    def _validate_surah(self, surah: int) -> None:
        """Validate surah number."""
        if not 1 <= surah <= 114:
            raise InvalidReferenceError(f"Invalid surah: {surah}. Must be 1-114.")

    def _validate_reference(self, surah: int, ayah: int) -> None:
        """Validate surah and ayah reference."""
        self._validate_surah(surah)
        max_ayah = VERSE_COUNTS[surah - 1]
        if not 1 <= ayah <= max_ayah:
            raise InvalidReferenceError(
                f"Invalid ayah: {ayah} for surah {surah}. Must be 1-{max_ayah}."
            )
