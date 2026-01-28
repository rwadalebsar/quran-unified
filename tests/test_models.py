"""Tests for data models."""

import json

import pytest

from quran_unified.models import Reciter, RecitationStyle, RevelationType, Surah, Tafsir, Verse


class TestVerse:
    """Tests for the Verse model."""

    def test_create_verse(self, sample_verse_data):
        verse = Verse(**sample_verse_data)
        assert verse.surah == 1
        assert verse.ayah == 1
        assert verse.arabic_uthmani == "بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ"

    def test_verse_reference(self, sample_verse):
        assert sample_verse.reference == "1:1"
        assert sample_verse.verse_key == "1:1"

    def test_verse_to_dict(self, sample_verse):
        data = sample_verse.to_dict()
        assert data["surah"] == 1
        assert data["ayah"] == 1
        assert data["reference"] == "1:1"
        assert data["verse_key"] == "1:1"

    def test_verse_to_json(self, sample_verse):
        json_str = sample_verse.to_json()
        data = json.loads(json_str)
        assert data["surah"] == 1
        assert data["ayah"] == 1

    def test_verse_from_dict(self, sample_verse_data):
        verse = Verse.from_dict(sample_verse_data)
        assert verse.surah == 1
        assert verse.ayah == 1

    def test_verse_default_values(self):
        verse = Verse(surah=1, ayah=1, arabic_uthmani="test")
        assert verse.arabic_simple == ""
        assert verse.translation == ""
        assert verse.audio_url == ""
        assert verse.audio_urls == {}
        assert verse.word_by_word == []
        assert verse.sajda is False


class TestSurah:
    """Tests for the Surah model."""

    def test_create_surah(self, sample_surah_data):
        surah = Surah(**sample_surah_data)
        assert surah.number == 1
        assert surah.name_arabic == "الفاتحة"
        assert surah.verses_count == 7

    def test_surah_revelation_type(self, sample_surah):
        assert sample_surah.revelation_type == RevelationType.MECCAN
        assert sample_surah.revelation_type.value == "Meccan"

    def test_surah_to_dict(self, sample_surah):
        data = sample_surah.to_dict()
        assert data["number"] == 1
        assert data["revelation_type"] == "Meccan"

    def test_surah_from_dict(self):
        data = {
            "number": 2,
            "name_arabic": "البقرة",
            "name_english": "The Cow",
            "name_transliteration": "Al-Baqarah",
            "verses_count": 286,
            "revelation_type": "Medinan",
            "revelation_order": 87,
            "pages": [2, 49],
        }
        surah = Surah.from_dict(data)
        assert surah.number == 2
        assert surah.revelation_type == RevelationType.MEDINAN
        assert surah.pages == (2, 49)


class TestTafsir:
    """Tests for the Tafsir model."""

    def test_create_tafsir(self, sample_tafsir_data):
        tafsir = Tafsir(**sample_tafsir_data)
        assert tafsir.id == 1
        assert tafsir.name == "Tafsir Ibn Kathir"
        assert tafsir.language == "ar"

    def test_tafsir_to_dict(self, sample_tafsir):
        data = sample_tafsir.to_dict()
        assert data["id"] == 1
        assert data["author"] == "Ibn Kathir"

    def test_tafsir_from_dict(self, sample_tafsir_data):
        tafsir = Tafsir.from_dict(sample_tafsir_data)
        assert tafsir.id == 1
        assert tafsir.text == "Sample tafsir text..."


class TestReciter:
    """Tests for the Reciter model."""

    def test_create_reciter(self, sample_reciter_data):
        reciter = Reciter(**sample_reciter_data)
        assert reciter.id == "alafasy"
        assert reciter.name_english == "Mishary Rashid Alafasy"

    def test_reciter_style(self, sample_reciter):
        assert sample_reciter.style == RecitationStyle.MURATTAL
        assert sample_reciter.style.value == "Murattal"

    def test_reciter_to_dict(self, sample_reciter):
        data = sample_reciter.to_dict()
        assert data["id"] == "alafasy"
        assert data["style"] == "Murattal"

    def test_reciter_from_dict(self):
        data = {
            "id": "husary",
            "name_arabic": "محمود خليل الحصري",
            "name_english": "Mahmoud Khalil Al-Husary",
            "style": "Muallim",
            "bitrate": 128,
        }
        reciter = Reciter.from_dict(data)
        assert reciter.id == "husary"
        assert reciter.style == RecitationStyle.MUALLIM
