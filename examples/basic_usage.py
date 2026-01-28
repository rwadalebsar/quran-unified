#!/usr/bin/env python3
"""Basic usage examples for quran-unified."""

from quran_unified import QuranAPI


def main():
    """Demonstrate basic usage of QuranAPI."""

    # Using context manager (recommended)
    with QuranAPI() as quran:
        # =====================
        # Getting a Single Verse
        # =====================
        print("=" * 50)
        print("Getting Ayat al-Kursi (2:255)")
        print("=" * 50)

        verse = quran.get_verse(2, 255)
        print(f"Reference: {verse.reference}")
        print(f"Arabic: {verse.arabic_uthmani}")
        print(f"Translation: {verse.translation}")
        print(f"Audio: {verse.audio_url}")
        print()

        # =====================
        # Getting Surah Info
        # =====================
        print("=" * 50)
        print("Getting Al-Fatihah Info")
        print("=" * 50)

        surah = quran.get_surah_info(1)
        print(f"Name: {surah.name_english} ({surah.name_arabic})")
        print(f"Transliteration: {surah.name_transliteration}")
        print(f"Verses: {surah.verses_count}")
        print(f"Revelation: {surah.revelation_type.value}")
        print(f"Revelation Order: {surah.revelation_order}")
        print(f"Pages: {surah.pages[0]}-{surah.pages[1]}")
        print()

        # =====================
        # Getting a Full Surah
        # =====================
        print("=" * 50)
        print("Getting Al-Fatihah with Verses")
        print("=" * 50)

        surah = quran.get_surah(1)
        print(f"{surah.name_english}")
        print("-" * 30)
        for verse in surah.verses:
            print(f"[{verse.ayah}] {verse.arabic_uthmani}")
            print(f"    {verse.translation}")
            print()

        # =====================
        # Getting a Range of Verses
        # =====================
        print("=" * 50)
        print("Getting Al-Baqarah 1-5")
        print("=" * 50)

        verses = quran.get_verses(2, 1, 5)
        for v in verses:
            print(f"[{v.reference}] {v.arabic_uthmani}")
        print()

        # =====================
        # Random Verse
        # =====================
        print("=" * 50)
        print("Random Verse")
        print("=" * 50)

        random_verse = quran.get_random_verse()
        print(f"[{random_verse.reference}] {random_verse.arabic_uthmani}")
        print(f"Translation: {random_verse.translation}")
        print()

        # =====================
        # Audio URL
        # =====================
        print("=" * 50)
        print("Getting Audio URL")
        print("=" * 50)

        audio_url = quran.get_audio_url(1, 1, reciter="alafasy")
        print(f"Audio URL: {audio_url}")
        print()

        # =====================
        # List Reciters
        # =====================
        print("=" * 50)
        print("Available Reciters (first 5)")
        print("=" * 50)

        reciters = quran.get_available_reciters()
        for r in reciters[:5]:
            print(f"  {r.id}: {r.name_english} ({r.style.value})")
        print(f"  ... and {len(reciters) - 5} more")
        print()


if __name__ == "__main__":
    main()
