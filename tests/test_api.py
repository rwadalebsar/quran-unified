"""Tests for the main QuranAPI class."""

import pytest
import responses

from quran_unified import QuranAPI
from quran_unified.exceptions import InvalidReferenceError


class TestQuranAPIValidation:
    """Tests for input validation."""

    def test_invalid_surah_too_low(self, quran_api):
        with pytest.raises(InvalidReferenceError):
            quran_api.get_verse(0, 1)

    def test_invalid_surah_too_high(self, quran_api):
        with pytest.raises(InvalidReferenceError):
            quran_api.get_verse(115, 1)

    def test_invalid_ayah_too_low(self, quran_api):
        with pytest.raises(InvalidReferenceError):
            quran_api.get_verse(1, 0)

    def test_invalid_ayah_too_high(self, quran_api):
        with pytest.raises(InvalidReferenceError):
            quran_api.get_verse(1, 10)  # Al-Fatihah has only 7 verses

    def test_invalid_juz(self, quran_api):
        with pytest.raises(InvalidReferenceError):
            quran_api.get_juz(31)

    def test_invalid_hizb(self, quran_api):
        with pytest.raises(InvalidReferenceError):
            quran_api.get_hizb(61)

    def test_invalid_page(self, quran_api):
        with pytest.raises(InvalidReferenceError):
            quran_api.get_page(605)


class TestQuranAPISurahInfo:
    """Tests for surah metadata (uses constants, no API calls)."""

    def test_get_surah_info(self, quran_api):
        surah = quran_api.get_surah_info(1)
        assert surah.number == 1
        assert surah.name_arabic == "الفاتحة"
        assert surah.name_english == "The Opening"
        assert surah.verses_count == 7

    def test_get_surah_info_baqarah(self, quran_api):
        surah = quran_api.get_surah_info(2)
        assert surah.number == 2
        assert surah.name_english == "The Cow"
        assert surah.verses_count == 286

    def test_get_all_surahs(self, quran_api):
        surahs = quran_api.get_all_surahs()
        assert len(surahs) == 114
        assert surahs[0].number == 1
        assert surahs[113].number == 114

    def test_get_verse_count(self, quran_api):
        assert quran_api.get_verse_count(1) == 7
        assert quran_api.get_verse_count(2) == 286
        assert quran_api.get_verse_count(114) == 6


class TestQuranAPIReciters:
    """Tests for reciter listing (uses constants, no API calls)."""

    def test_get_available_reciters(self, quran_api):
        reciters = quran_api.get_available_reciters()
        assert len(reciters) > 0

        # Check for known reciters
        reciter_ids = [r.id for r in reciters]
        assert "alafasy" in reciter_ids
        assert "husary" in reciter_ids

    def test_reciter_has_required_fields(self, quran_api):
        reciters = quran_api.get_available_reciters()
        for r in reciters:
            assert r.id
            assert r.name_arabic
            assert r.name_english
            assert r.style


class TestQuranAPIAudioUrls:
    """Tests for audio URL generation (no API calls)."""

    def test_get_audio_url(self, quran_api):
        url = quran_api.get_audio_url(1, 1, reciter="alafasy")
        assert "everyayah.com" in url
        assert "001001.mp3" in url

    def test_get_surah_audio_urls(self, quran_api):
        urls = quran_api.get_surah_audio_urls(1)
        assert len(urls) == 7  # Al-Fatihah has 7 verses
        assert "001001.mp3" in urls[0]
        assert "001007.mp3" in urls[6]

    def test_audio_url_different_reciters(self, quran_api):
        url1 = quran_api.get_audio_url(1, 1, reciter="alafasy")
        url2 = quran_api.get_audio_url(1, 1, reciter="husary")
        assert url1 != url2


class TestQuranAPIContextManager:
    """Tests for context manager protocol."""

    def test_context_manager(self):
        with QuranAPI(cache_backend="none") as api:
            surah = api.get_surah_info(1)
            assert surah.number == 1

    def test_cache_backend_memory(self):
        api = QuranAPI(cache_backend="memory")
        assert api._cache is not None
        api.close()

    def test_cache_backend_none(self):
        api = QuranAPI(cache_backend="none")
        api.close()


class TestQuranAPICache:
    """Tests for caching behavior."""

    def test_clear_cache(self, quran_api):
        # Should not raise
        quran_api.clear_cache()


@responses.activate
class TestQuranAPIWithMocking:
    """Tests that mock API responses."""

    def test_get_verse_mocked(self):
        # Mock AlQuran Cloud response
        responses.add(
            responses.GET,
            "https://api.alquran.cloud/v1/ayah/1:1/quran-uthmani",
            json={
                "code": 200,
                "status": "OK",
                "data": {
                    "text": "بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ",
                    "juz": 1,
                    "page": 1,
                    "hizbQuarter": 1,
                    "manzil": 1,
                    "ruku": 1,
                    "sajda": False,
                },
            },
        )

        # Mock translation response
        responses.add(
            responses.GET,
            "https://api.alquran.cloud/v1/ayah/1:1/en.sahih",
            json={
                "code": 200,
                "status": "OK",
                "data": {
                    "text": "In the name of Allah, the Entirely Merciful, the Especially Merciful.",
                },
            },
        )

        with QuranAPI(cache_backend="none") as api:
            verse = api.get_verse(1, 1)
            assert verse.surah == 1
            assert verse.ayah == 1
            assert "بِسْمِ" in verse.arabic_uthmani
            assert verse.audio_url  # Should have audio URL

    def test_search_mocked(self):
        responses.add(
            responses.GET,
            "https://api.quran.com/api/v4/search",
            json={
                "search": {
                    "results": [
                        {
                            "verse_key": "1:1",
                            "text": "بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ",
                            "translations": [{"text": "In the name of Allah..."}],
                        }
                    ]
                }
            },
        )

        with QuranAPI(cache_backend="none") as api:
            results = api.search("بسم", language="ar")
            assert len(results) > 0
            assert results[0].surah == 1
