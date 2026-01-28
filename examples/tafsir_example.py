#!/usr/bin/env python3
"""Tafsir (commentary) examples for quran-unified."""

from quran_unified import QuranAPI


def main():
    """Demonstrate tafsir functionality."""

    with QuranAPI() as quran:
        # =====================
        # Get Available Tafsirs
        # =====================
        print("=" * 50)
        print("Available Tafsirs")
        print("=" * 50)

        tafsirs = quran.get_available_tafsirs()
        for t in tafsirs[:10]:
            print(f"  ID {t.id}: {t.name}")
            if t.author:
                print(f"       Author: {t.author}")
        if len(tafsirs) > 10:
            print(f"  ... and {len(tafsirs) - 10} more")
        print()

        # =====================
        # Get Tafsir for Ayat al-Kursi
        # =====================
        print("=" * 50)
        print("Tafsir for Ayat al-Kursi (2:255)")
        print("=" * 50)

        tafsir = quran.get_tafsir(2, 255, tafsir_id=1)
        print(f"Source: {tafsir.name}")
        if tafsir.author:
            print(f"Author: {tafsir.author}")
        print(f"\nTafsir text:")
        print("-" * 40)
        # Print first 500 characters
        text = tafsir.text[:500] + "..." if len(tafsir.text) > 500 else tafsir.text
        print(text)
        print()

        # =====================
        # Get Tafsir for Al-Fatihah
        # =====================
        print("=" * 50)
        print("Tafsir for Al-Fatihah (all verses)")
        print("=" * 50)

        tafsir_list = quran.get_tafsir_range(1, 1, 7, tafsir_id=1)
        for i, t in enumerate(tafsir_list, 1):
            print(f"\nVerse {i}:")
            print("-" * 20)
            text = t.text[:200] + "..." if len(t.text) > 200 else t.text
            print(text)
        print()

        # =====================
        # Get Verse with Tafsir Included
        # =====================
        print("=" * 50)
        print("Verse with embedded tafsir")
        print("=" * 50)

        verse = quran.get_verse(1, 1, include_tafsir=True, tafsir_id=1)
        print(f"Verse: {verse.arabic_uthmani}")
        print(f"Translation: {verse.translation}")
        print(f"\nTafsir:")
        if verse.tafsir:
            text = verse.tafsir[:300] + "..." if len(verse.tafsir) > 300 else verse.tafsir
            print(text)
        else:
            print("(No tafsir available)")


if __name__ == "__main__":
    main()
