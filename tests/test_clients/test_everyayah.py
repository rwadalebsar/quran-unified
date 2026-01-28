"""Tests for EveryAyahClient."""

import pytest

from quran_unified.clients.everyayah import EveryAyahClient
from quran_unified.exceptions import InvalidReferenceError


class TestEveryAyahClient:
    """Tests for the EveryAyah audio URL client."""

    @pytest.fixture
    def client(self):
        return EveryAyahClient()

    def test_get_audio_url(self, client):
        url = client.get_audio_url(1, 1, "alafasy")
        assert url == "https://everyayah.com/data/Alafasy_128kbps/001001.mp3"

    def test_get_audio_url_different_verse(self, client):
        url = client.get_audio_url(2, 255, "alafasy")
        assert url == "https://everyayah.com/data/Alafasy_128kbps/002255.mp3"

    def test_get_audio_url_different_reciter(self, client):
        url = client.get_audio_url(1, 1, "husary")
        assert "Husary_128kbps" in url

    def test_get_surah_audio_urls(self, client):
        urls = client.get_surah_audio_urls(1, 7, "alafasy")
        assert len(urls) == 7
        assert "001001.mp3" in urls[0]
        assert "001007.mp3" in urls[6]

    def test_get_available_reciters(self, client):
        reciters = client.get_available_reciters()
        assert "alafasy" in reciters
        assert "husary" in reciters
        assert len(reciters) > 10

    def test_invalid_reciter(self, client):
        with pytest.raises(InvalidReferenceError):
            client.get_audio_url(1, 1, "nonexistent_reciter")

    def test_url_format_padding(self, client):
        # Test that surah and ayah are zero-padded to 3 digits
        url = client.get_audio_url(1, 1, "alafasy")
        assert "001001" in url

        url = client.get_audio_url(114, 6, "alafasy")
        assert "114006" in url
