# Quick Start Guide

This guide will help you get started with `quran-unified` in just a few minutes.

## Installation

```bash
pip install quran-unified
```

## Your First Script

Create a file called `my_quran_app.py`:

```python
from quran_unified import QuranAPI

# Initialize the API
with QuranAPI() as quran:
    # Get the first verse of Al-Fatihah
    verse = quran.get_verse(1, 1)

    print("=== Bismillah ===")
    print(f"Arabic: {verse.arabic_uthmani}")
    print(f"Translation: {verse.translation}")
    print(f"Reference: {verse.reference}")
```

Run it:

```bash
python my_quran_app.py
```

Output:
```
=== Bismillah ===
Arabic: بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ
Translation: In the name of Allah, the Entirely Merciful, the Especially Merciful.
Reference: 1:1
```

## Common Tasks

### Get a Specific Verse

```python
# Ayat al-Kursi (The Throne Verse)
verse = quran.get_verse(2, 255)
print(verse.arabic_uthmani)
print(verse.translation)
```

### Get an Entire Surah

```python
# Get Al-Fatihah with all verses
surah = quran.get_surah(1)

print(f"{surah.name_english} - {surah.name_arabic}")
print(f"Verses: {surah.verses_count}")

for verse in surah.verses:
    print(f"[{verse.ayah}] {verse.arabic_uthmani}")
    print(f"    {verse.translation}")
    print()
```

### Get Surah Information Only

```python
# Just metadata, no verses (faster)
surah = quran.get_surah_info(2)

print(f"Name: {surah.name_english}")
print(f"Arabic: {surah.name_arabic}")
print(f"Verses: {surah.verses_count}")
print(f"Type: {surah.revelation_type.value}")  # Meccan or Medinan
print(f"Revelation Order: {surah.revelation_order}")
print(f"Pages: {surah.pages[0]} - {surah.pages[1]}")
```

### Get Audio URL

```python
# Get audio for verse 1:1 by Mishary Alafasy
audio_url = quran.get_audio_url(1, 1, reciter="alafasy")
print(audio_url)
# https://everyayah.com/data/Alafasy_128kbps/001001.mp3

# Get all audio URLs for a surah
urls = quran.get_surah_audio_urls(1, reciter="alafasy")
for i, url in enumerate(urls, 1):
    print(f"Verse {i}: {url}")
```

### Search the Quran

```python
# Search in English
results = quran.search("mercy", language="en", limit=5)

for verse in results:
    print(f"[{verse.reference}] {verse.translation[:100]}...")
```

### Get a Random Verse

```python
verse = quran.get_random_verse()
print(f"[{verse.reference}] {verse.arabic_uthmani}")
print(f"Translation: {verse.translation}")
```

## Using the CLI

After installation, you can use the `quran` command:

```bash
# Get a verse
quran verse 2:255

# Get surah info
quran surah 1 --info-only

# Search
quran search "paradise" --limit 5

# Get audio URL
quran audio 1:1 --reciter alafasy

# List reciters
quran reciters

# Get JSON output
quran verse 1:1 --json
```

## Next Steps

- Read the [full documentation](api_reference.md) for all available methods
- Check out the [examples](../examples/) for more complex use cases
- See the [CLI documentation](cli.md) for command-line usage
