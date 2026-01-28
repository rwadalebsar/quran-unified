"""Tests for TafseerAPIClient."""

import pytest
import responses

from quran_unified.clients.tafseer_api import TafseerAPIClient


@responses.activate
class TestTafseerAPIClient:
    """Tests for the Tafseer API client."""

    def test_get_tafsirs(self):
        responses.add(
            responses.GET,
            "http://api.quran-tafseer.com/tafseer",
            json=[
                {"id": 1, "name": "التفسير الميسر", "author": "نخبة من العلماء"},
            ],
        )

        with TafseerAPIClient() as client:
            tafsirs = client.get_tafsirs()
            assert len(tafsirs) > 0

    def test_get_tafsir(self):
        responses.add(
            responses.GET,
            "http://api.quran-tafseer.com/tafseer/1/1/1",
            json={
                "tafsir_id": 1,
                "text": "Sample tafsir text...",
            },
        )

        with TafseerAPIClient() as client:
            data = client.get_tafsir(1, 1, 1)
            assert "text" in data

    def test_get_tafsir_range(self):
        responses.add(
            responses.GET,
            "http://api.quran-tafseer.com/tafseer/1/1/1/3",
            json=[
                {"aya": 1, "text": "Tafsir 1"},
                {"aya": 2, "text": "Tafsir 2"},
                {"aya": 3, "text": "Tafsir 3"},
            ],
        )

        with TafseerAPIClient() as client:
            data = client.get_tafsir_range(1, 1, 1, 3)
            assert len(data) == 3
