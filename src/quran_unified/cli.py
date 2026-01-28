"""Command Line Interface for quran-unified.

Usage:
    quran verse 2:255
    quran verse 2:255 --translation en.sahih --json
    quran surah 1
    quran surah 1 --translation ar.muyassar
    quran search "الرحمن"
    quran tafsir 2:255 --tafsir-id 1
    quran audio 1:1 --reciter alafasy
    quran reciters
    quran translations --language ar
"""

import json
import sys
from typing import Optional

import click

from quran_unified.api import QuranAPI
from quran_unified.exceptions import InvalidReferenceError, QuranAPIError


def parse_reference(reference: str) -> tuple:
    """Parse a verse reference like '2:255' into (surah, ayah)."""
    try:
        parts = reference.split(":")
        if len(parts) != 2:
            raise ValueError("Invalid format")
        return int(parts[0]), int(parts[1])
    except (ValueError, IndexError):
        raise click.BadParameter(
            f"Invalid reference '{reference}'. Use format surah:ayah (e.g., 2:255)"
        )


@click.group()
@click.version_option(package_name="quran-unified")
def cli():
    """Quran Unified CLI - Access Quran data from multiple sources."""
    pass


@cli.command()
@click.argument("reference")
@click.option("--translation", "-t", default="en.sahih", help="Translation identifier")
@click.option("--reciter", "-r", default="alafasy", help="Reciter identifier")
@click.option("--tafsir", is_flag=True, help="Include tafsir")
@click.option("--tafsir-id", "-i", type=int, default=1, help="Tafsir ID")
@click.option("--json", "as_json", is_flag=True, help="Output as JSON")
def verse(
    reference: str,
    translation: str,
    reciter: str,
    tafsir: bool,
    tafsir_id: int,
    as_json: bool,
):
    """Get a verse by reference (e.g., 2:255)."""
    surah, ayah = parse_reference(reference)

    try:
        with QuranAPI(cache_backend="none") as api:
            v = api.get_verse(
                surah,
                ayah,
                translation=translation,
                reciter=reciter,
                include_tafsir=tafsir,
                tafsir_id=tafsir_id,
            )

            if as_json:
                click.echo(v.to_json())
            else:
                click.echo(f"\n[{v.reference}] {v.arabic_uthmani}\n")
                if v.translation:
                    click.echo(f"Translation: {v.translation}\n")
                if v.audio_url:
                    click.echo(f"Audio: {v.audio_url}")
                if tafsir and v.tafsir:
                    click.echo(f"\nTafsir:\n{v.tafsir}")

    except InvalidReferenceError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)
    except QuranAPIError as e:
        click.echo(f"API Error: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.argument("number", type=int)
@click.option("--translation", "-t", default="en.sahih", help="Translation identifier")
@click.option("--json", "as_json", is_flag=True, help="Output as JSON")
@click.option("--info-only", is_flag=True, help="Only show surah info, not verses")
def surah(number: int, translation: str, as_json: bool, info_only: bool):
    """Get a surah by number (1-114)."""
    try:
        with QuranAPI(cache_backend="none") as api:
            s = api.get_surah(number, translation=translation, include_verses=not info_only)

            if as_json:
                click.echo(json.dumps(s.to_dict(), ensure_ascii=False, indent=2))
            else:
                click.echo(f"\n{s.name_arabic} - {s.name_english} ({s.name_transliteration})")
                click.echo(f"Verses: {s.verses_count} | {s.revelation_type.value} | Order: {s.revelation_order}")
                click.echo(f"Pages: {s.pages[0]}-{s.pages[1]}\n")

                if not info_only and s.verses:
                    for v in s.verses:
                        click.echo(f"[{v.ayah}] {v.arabic_uthmani}")
                        if v.translation:
                            click.echo(f"    {v.translation}\n")

    except InvalidReferenceError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)
    except QuranAPIError as e:
        click.echo(f"API Error: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.argument("query")
@click.option("--language", "-l", default="en", help="Search language")
@click.option("--limit", default=10, help="Maximum results")
@click.option("--json", "as_json", is_flag=True, help="Output as JSON")
def search(query: str, language: str, limit: int, as_json: bool):
    """Search the Quran for text."""
    try:
        with QuranAPI(cache_backend="none") as api:
            results = api.search(query, language=language, limit=limit)

            if as_json:
                click.echo(json.dumps([v.to_dict() for v in results], ensure_ascii=False, indent=2))
            else:
                click.echo(f"\nFound {len(results)} results for '{query}':\n")
                for v in results:
                    click.echo(f"[{v.reference}] {v.arabic_uthmani}")
                    if v.translation:
                        click.echo(f"    {v.translation}")
                    click.echo()

    except QuranAPIError as e:
        click.echo(f"API Error: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.argument("reference")
@click.option("--tafsir-id", "-i", type=int, default=1, help="Tafsir ID")
@click.option("--json", "as_json", is_flag=True, help="Output as JSON")
def tafsir(reference: str, tafsir_id: int, as_json: bool):
    """Get tafsir for a verse (e.g., 2:255)."""
    surah, ayah = parse_reference(reference)

    try:
        with QuranAPI(cache_backend="none") as api:
            t = api.get_tafsir(surah, ayah, tafsir_id=tafsir_id)

            if as_json:
                click.echo(json.dumps(t.to_dict(), ensure_ascii=False, indent=2))
            else:
                click.echo(f"\nTafsir for {surah}:{ayah}")
                if t.name:
                    click.echo(f"Source: {t.name} by {t.author}\n")
                click.echo(t.text)

    except InvalidReferenceError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)
    except QuranAPIError as e:
        click.echo(f"API Error: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.argument("reference")
@click.option("--reciter", "-r", default="alafasy", help="Reciter identifier")
def audio(reference: str, reciter: str):
    """Get audio URL for a verse (e.g., 1:1)."""
    surah, ayah = parse_reference(reference)

    try:
        with QuranAPI(cache_backend="none") as api:
            url = api.get_audio_url(surah, ayah, reciter=reciter)
            click.echo(url)

    except InvalidReferenceError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.option("--json", "as_json", is_flag=True, help="Output as JSON")
def reciters(as_json: bool):
    """List available reciters."""
    with QuranAPI(cache_backend="none") as api:
        recs = api.get_available_reciters()

        if as_json:
            click.echo(json.dumps([r.to_dict() for r in recs], ensure_ascii=False, indent=2))
        else:
            click.echo("\nAvailable Reciters:\n")
            for r in recs:
                click.echo(f"  {r.id}: {r.name_english} ({r.name_arabic}) - {r.style.value}")


@cli.command()
@click.option("--language", "-l", default=None, help="Filter by language code")
@click.option("--json", "as_json", is_flag=True, help="Output as JSON")
def translations(language: Optional[str], as_json: bool):
    """List available translations."""
    try:
        with QuranAPI(cache_backend="none") as api:
            trans = api.get_available_translations(language=language)

            if as_json:
                click.echo(json.dumps(trans, ensure_ascii=False, indent=2))
            else:
                click.echo("\nAvailable Translations:\n")
                for t in trans[:30]:  # Limit output
                    name = t.get("name") or t.get("englishName", "")
                    identifier = t.get("identifier") or t.get("id", "")
                    lang = t.get("language") or t.get("language_name", "")
                    click.echo(f"  {identifier}: {name} ({lang})")

                if len(trans) > 30:
                    click.echo(f"\n  ... and {len(trans) - 30} more (use --json for full list)")

    except QuranAPIError as e:
        click.echo(f"API Error: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.option("--json", "as_json", is_flag=True, help="Output as JSON")
def tafsirs(as_json: bool):
    """List available tafsirs."""
    try:
        with QuranAPI(cache_backend="none") as api:
            tlist = api.get_available_tafsirs()

            if as_json:
                click.echo(json.dumps([t.to_dict() for t in tlist], ensure_ascii=False, indent=2))
            else:
                click.echo("\nAvailable Tafsirs:\n")
                for t in tlist:
                    click.echo(f"  {t.id}: {t.name} by {t.author} ({t.language})")

    except QuranAPIError as e:
        click.echo(f"API Error: {e}", err=True)
        sys.exit(1)


if __name__ == "__main__":
    cli()
