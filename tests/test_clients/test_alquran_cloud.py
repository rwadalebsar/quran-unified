"""Tests for AlQuranCloudClient."""

import pytest
import responses

from quran_unified.clients.alquran_cloud import AlQuranCloudClient
from quran_unified.exceptions import QuranAPIError


@responses.activate
class TestAlQuranCloudClient:
    """Tests for the AlQuran Cloud API client."""

    def test_get_verse(self):
        responses.add(
            responses.GET,
            "https://api.alquran.cloud/v1/ayah/1:1/quran-uthmani",
            json={
                "code": 200,
                "status": "OK",
                "data": {
                    "number": 1,
                    "text": "بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ",
                    "surah": {"number": 1},
                    "numberInSurah": 1,
                },
            },
        )

        with AlQuranCloudClient() as client:
            data = client.get_verse(1, 1)
            assert data["text"] == "بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ"

    def test_get_surah(self):
        responses.add(
            responses.GET,
            "https://api.alquran.cloud/v1/surah/1/quran-uthmani",
            json={
                "code": 200,
                "status": "OK",
                "data": {
                    "number": 1,
                    "name": "الفاتحة",
                    "ayahs": [{"number": 1, "text": "بِسْمِ اللَّهِ"}],
                },
            },
        )

        with AlQuranCloudClient() as client:
            data = client.get_surah(1)
            assert data["number"] == 1

    def test_get_editions(self):
        responses.add(
            responses.GET,
            "https://api.alquran.cloud/v1/edition",
            json={
                "code": 200,
                "status": "OK",
                "data": [
                    {"identifier": "quran-uthmani", "language": "ar"},
                    {"identifier": "en.sahih", "language": "en"},
                ],
            },
        )

        with AlQuranCloudClient() as client:
            editions = client.get_editions()
            assert len(editions) == 2

    def test_search(self):
        responses.add(
            responses.GET,
            "https://api.alquran.cloud/v1/search/الله/en.sahih",
            json={
                "code": 200,
                "status": "OK",
                "data": {
                    "count": 10,
                    "matches": [{"text": "test"}],
                },
            },
        )

        with AlQuranCloudClient() as client:
            data = client.search("الله", edition="en.sahih")
            assert "count" in data

    def test_api_error(self):
        responses.add(
            responses.GET,
            "https://api.alquran.cloud/v1/ayah/999:1/quran-uthmani",
            json={
                "code": 404,
                "status": "Not Found",
                "data": None,
            },
        )

        with AlQuranCloudClient() as client:
            with pytest.raises(QuranAPIError):
                client.get_verse(999, 1)
