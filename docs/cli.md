# Command Line Interface

The `quran-unified` package includes a powerful CLI tool for quick access to Quran data from your terminal.

## Installation

The CLI is automatically installed with the package:

```bash
pip install quran-unified
```

## Commands Overview

```bash
quran --help
```

```
Usage: quran [OPTIONS] COMMAND [ARGS]...

  Quran Unified CLI - Access Quran data from multiple sources.

Options:
  --version  Show the version and exit.
  --help     Show this message and exit.

Commands:
  audio         Get audio URL for a verse
  reciters      List available reciters
  search        Search the Quran for text
  surah         Get a surah by number
  tafsir        Get tafsir for a verse
  tafsirs       List available tafsirs
  translations  List available translations
  verse         Get a verse by reference
```

---

## verse

Get a verse by reference.

```bash
quran verse REFERENCE [OPTIONS]
```

**Arguments:**
- `REFERENCE`: Verse reference in `surah:ayah` format (e.g., `2:255`)

**Options:**
- `-t, --translation TEXT`: Translation ID (default: `en.sahih`)
- `-r, --reciter TEXT`: Reciter ID (default: `alafasy`)
- `--tafsir`: Include tafsir
- `-i, --tafsir-id INTEGER`: Tafsir ID (default: `1`)
- `--json`: Output as JSON

**Examples:**

```bash
# Get a verse
quran verse 2:255

# With specific translation
quran verse 1:1 --translation en.sahih

# Include tafsir
quran verse 2:255 --tafsir

# JSON output
quran verse 1:1 --json
```

---

## surah

Get a surah by number.

```bash
quran surah NUMBER [OPTIONS]
```

**Arguments:**
- `NUMBER`: Surah number (1-114)

**Options:**
- `-t, --translation TEXT`: Translation ID (default: `en.sahih`)
- `--json`: Output as JSON
- `--info-only`: Only show surah info, not verses

**Examples:**

```bash
# Get full surah with verses
quran surah 1

# Get surah info only (faster)
quran surah 1 --info-only

# With different translation
quran surah 1 --translation ar.muyassar

# JSON output
quran surah 1 --json
```

---

## search

Search the Quran for text.

```bash
quran search QUERY [OPTIONS]
```

**Arguments:**
- `QUERY`: Search query text

**Options:**
- `-l, --language TEXT`: Search language (default: `en`)
- `--limit INTEGER`: Maximum results (default: `10`)
- `--json`: Output as JSON

**Examples:**

```bash
# Search in English
quran search "mercy"

# Search in Arabic
quran search "الرحمن"

# Limit results
quran search "paradise" --limit 5

# JSON output
quran search "mercy" --json
```

---

## tafsir

Get tafsir for a verse.

```bash
quran tafsir REFERENCE [OPTIONS]
```

**Arguments:**
- `REFERENCE`: Verse reference in `surah:ayah` format

**Options:**
- `-i, --tafsir-id INTEGER`: Tafsir ID (default: `1`)
- `--json`: Output as JSON

**Examples:**

```bash
# Get tafsir for Ayat al-Kursi
quran tafsir 2:255

# With specific tafsir
quran tafsir 1:1 --tafsir-id 2

# JSON output
quran tafsir 2:255 --json
```

---

## audio

Get audio URL for a verse.

```bash
quran audio REFERENCE [OPTIONS]
```

**Arguments:**
- `REFERENCE`: Verse reference in `surah:ayah` format

**Options:**
- `-r, --reciter TEXT`: Reciter ID (default: `alafasy`)

**Examples:**

```bash
# Get audio URL
quran audio 1:1

# With different reciter
quran audio 1:1 --reciter husary
```

---

## reciters

List available reciters.

```bash
quran reciters [OPTIONS]
```

**Options:**
- `--json`: Output as JSON

**Examples:**

```bash
# List reciters
quran reciters

# JSON output
quran reciters --json
```

---

## translations

List available translations.

```bash
quran translations [OPTIONS]
```

**Options:**
- `-l, --language TEXT`: Filter by language code
- `--json`: Output as JSON

**Examples:**

```bash
# List all translations
quran translations

# Filter by language
quran translations --language ar

# JSON output
quran translations --json
```

---

## tafsirs

List available tafsirs.

```bash
quran tafsirs [OPTIONS]
```

**Options:**
- `--json`: Output as JSON

**Examples:**

```bash
# List tafsirs
quran tafsirs

# JSON output
quran tafsirs --json
```

---

## Examples

### Daily Verse Script

```bash
#!/bin/bash
# Get a random verse each day

echo "=== Verse of the Day ==="
quran verse $(shuf -i 1-114 -n 1):$(shuf -i 1-7 -n 1) 2>/dev/null || quran verse 1:1
```

### Download Audio for a Surah

```bash
#!/bin/bash
# Download all audio files for a surah

SURAH=1
RECITER=alafasy

for i in $(seq 1 7); do
    URL=$(quran audio ${SURAH}:${i} --reciter ${RECITER})
    echo "Downloading verse ${i}..."
    curl -O "${URL}"
done
```

### Export Surah to JSON

```bash
# Export Al-Fatihah to JSON file
quran surah 1 --json > fatihah.json
```

### Search and Save Results

```bash
# Search and save results
quran search "mercy" --limit 50 --json > mercy_verses.json
```
