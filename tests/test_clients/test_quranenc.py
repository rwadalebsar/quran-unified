"""Tests for QuranEncClient."""

import pytest
import responses

from quran_unified.clients.quranenc import QuranEncClient


@responses.activate
class TestQuranEncClient:
    """Tests for the QuranEnc API client."""

    def test_get_translations_list(self):
        responses.add(
            responses.GET,
            "https://quranenc.com/api/v1/translations/list",
            json=[
                {
                    "key": "english_saheeh",
                    "language_iso_code": "en",
                    "version": "1.0",
                    "last_update": 1234567890,
                    "title": "Sahih International",
                    "description": "English translation",
                },
            ],
        )

        with QuranEncClient() as client:
            translations = client.get_translations_list()
            assert len(translations) == 1
            assert translations[0]["key"] == "english_saheeh"

    def test_get_translations_list_by_language(self):
        responses.add(
            responses.GET,
            "https://quranenc.com/api/v1/translations/list/ar",
            json=[
                {
                    "key": "arabic_muyassar",
                    "language_iso_code": "ar",
                    "title": "التفسير الميسر",
                },
            ],
        )

        with QuranEncClient() as client:
            translations = client.get_translations_list(language="ar")
            assert translations[0]["language_iso_code"] == "ar"

    def test_get_sura_translation(self):
        responses.add(
            responses.GET,
            "https://quranenc.com/api/v1/translation/sura/english_saheeh/1",
            json=[
                {"sura": 1, "aya": 1, "translation": "In the name...", "footnotes": ""},
                {"sura": 1, "aya": 2, "translation": "All praise...", "footnotes": ""},
            ],
        )

        with QuranEncClient() as client:
            verses = client.get_sura_translation("english_saheeh", 1)
            assert len(verses) == 2
            assert verses[0]["sura"] == 1
            assert verses[0]["aya"] == 1

    def test_get_aya_translation(self):
        responses.add(
            responses.GET,
            "https://quranenc.com/api/v1/translation/aya/english_saheeh/1/1",
            json={
                "sura": 1,
                "aya": 1,
                "translation": "In the name of Allah, the Entirely Merciful, the Especially Merciful.",
                "footnotes": "",
            },
        )

        with QuranEncClient() as client:
            verse = client.get_aya_translation("english_saheeh", 1, 1)
            assert verse["sura"] == 1
            assert verse["aya"] == 1
            assert "Allah" in verse["translation"]
