"""Tests for QuranComClient."""

import pytest
import responses

from quran_unified.clients.quran_com import QuranComClient


@responses.activate
class TestQuranComClient:
    """Tests for the Quran.com API client."""

    def test_get_verse(self):
        responses.add(
            responses.GET,
            "https://api.quran.com/api/v4/verses/by_key/1:1",
            json={
                "verse": {
                    "id": 1,
                    "verse_key": "1:1",
                    "text_uthmani": "بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ",
                }
            },
        )

        with QuranComClient() as client:
            data = client.get_verse(1, 1)
            assert "verse" in data

    def test_get_chapters(self):
        responses.add(
            responses.GET,
            "https://api.quran.com/api/v4/chapters",
            json={
                "chapters": [
                    {"id": 1, "name_simple": "Al-Fatihah"},
                    {"id": 2, "name_simple": "Al-Baqarah"},
                ]
            },
        )

        with QuranComClient() as client:
            chapters = client.get_chapters()
            assert len(chapters) == 2

    def test_get_translations(self):
        responses.add(
            responses.GET,
            "https://api.quran.com/api/v4/resources/translations",
            json={
                "translations": [
                    {"id": 131, "name": "Sahih International"},
                ]
            },
        )

        with QuranComClient() as client:
            translations = client.get_translations("en")
            assert len(translations) > 0

    def test_search(self):
        responses.add(
            responses.GET,
            "https://api.quran.com/api/v4/search",
            json={
                "search": {
                    "query": "mercy",
                    "total_results": 10,
                    "results": [{"verse_key": "1:1"}],
                }
            },
        )

        with QuranComClient() as client:
            data = client.search("mercy")
            assert "search" in data
