#!/usr/bin/env python3
"""Search examples for quran-unified."""

from quran_unified import QuranAPI


def main():
    """Demonstrate search functionality."""

    with QuranAPI() as quran:
        # =====================
        # Search in English
        # =====================
        print("=" * 50)
        print("Searching for 'mercy' in English")
        print("=" * 50)

        results = quran.search("mercy", language="en", limit=5)
        print(f"Found {len(results)} results:\n")

        for verse in results:
            print(f"[{verse.reference}]")
            print(f"  {verse.translation[:100]}...")
            print()

        # =====================
        # Search in Arabic
        # =====================
        print("=" * 50)
        print("Searching for 'الرحمن' in Arabic")
        print("=" * 50)

        results = quran.search("الرحمن", language="ar", limit=5)
        print(f"Found {len(results)} results:\n")

        for verse in results:
            print(f"[{verse.reference}] {verse.arabic_uthmani}")
            print()

        # =====================
        # Search for Specific Terms
        # =====================
        print("=" * 50)
        print("Searching for 'paradise' and 'hellfire'")
        print("=" * 50)

        for term in ["paradise", "hellfire"]:
            results = quran.search(term, language="en", limit=3)
            print(f"\n'{term}' ({len(results)} results):")
            for verse in results:
                print(f"  [{verse.reference}] {verse.translation[:80]}...")


if __name__ == "__main__":
    main()
