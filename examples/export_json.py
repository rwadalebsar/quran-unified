#!/usr/bin/env python3
"""Export Quran data to JSON files."""

import json
from pathlib import Path

from quran_unified import QuranAPI


def export_surah_to_json(quran: QuranAPI, surah_num: int, output_dir: Path):
    """Export a surah to a JSON file."""
    surah = quran.get_surah(surah_num)
    data = surah.to_dict()

    filename = output_dir / f"surah_{surah_num:03d}_{surah.name_transliteration.lower().replace(' ', '_')}.json"

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"Exported: {filename}")
    return filename


def export_all_surah_info(quran: QuranAPI, output_file: Path):
    """Export metadata for all 114 surahs."""
    surahs = quran.get_all_surahs()
    data = [s.to_dict() for s in surahs]

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"Exported all surah info: {output_file}")


def main():
    """Export examples."""
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)

    with QuranAPI() as quran:
        # Export Al-Fatihah
        print("=" * 50)
        print("Exporting Al-Fatihah to JSON")
        print("=" * 50)
        export_surah_to_json(quran, 1, output_dir)
        print()

        # Export Al-Ikhlas
        print("=" * 50)
        print("Exporting Al-Ikhlas to JSON")
        print("=" * 50)
        export_surah_to_json(quran, 112, output_dir)
        print()

        # Export all surah metadata
        print("=" * 50)
        print("Exporting all surah metadata")
        print("=" * 50)
        export_all_surah_info(quran, output_dir / "all_surahs.json")
        print()

        # Export a single verse
        print("=" * 50)
        print("Exporting Ayat al-Kursi")
        print("=" * 50)
        verse = quran.get_verse(2, 255)
        verse_file = output_dir / "ayat_al_kursi.json"

        with open(verse_file, "w", encoding="utf-8") as f:
            f.write(verse.to_json())

        print(f"Exported: {verse_file}")


if __name__ == "__main__":
    main()
