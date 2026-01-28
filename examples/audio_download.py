#!/usr/bin/env python3
"""Download audio recitations example."""

import urllib.request
from pathlib import Path

from quran_unified import QuranAPI


def download_verse_audio(url: str, output_path: Path) -> bool:
    """Download audio file from URL."""
    try:
        urllib.request.urlretrieve(url, output_path)
        return True
    except Exception as e:
        print(f"Error downloading {url}: {e}")
        return False


def main():
    """Download audio examples."""
    output_dir = Path("audio")
    output_dir.mkdir(exist_ok=True)

    with QuranAPI() as quran:
        # =====================
        # Download Single Verse
        # =====================
        print("=" * 50)
        print("Downloading audio for Al-Fatihah verse 1")
        print("=" * 50)

        url = quran.get_audio_url(1, 1, reciter="alafasy")
        output_file = output_dir / "001001_alafasy.mp3"

        print(f"URL: {url}")
        print(f"Downloading to: {output_file}")

        if download_verse_audio(url, output_file):
            print("Download complete!")
        print()

        # =====================
        # Get All URLs for a Surah
        # =====================
        print("=" * 50)
        print("Audio URLs for Al-Fatihah (not downloading)")
        print("=" * 50)

        urls = quran.get_surah_audio_urls(1, reciter="alafasy")
        for i, url in enumerate(urls, 1):
            print(f"  Verse {i}: {url}")
        print()

        # =====================
        # Download Different Reciters
        # =====================
        print("=" * 50)
        print("Comparing reciters for verse 1:1")
        print("=" * 50)

        reciters = ["alafasy", "husary", "minshawi", "sudais"]
        for reciter in reciters:
            url = quran.get_audio_url(1, 1, reciter=reciter)
            print(f"  {reciter}: {url}")
        print()

        # =====================
        # List Available Reciters
        # =====================
        print("=" * 50)
        print("All available reciters")
        print("=" * 50)

        all_reciters = quran.get_available_reciters()
        for r in all_reciters:
            print(f"  {r.id}: {r.name_english} - {r.name_arabic} ({r.style.value})")


if __name__ == "__main__":
    main()
