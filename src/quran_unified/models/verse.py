"""Verse data model."""

import json
from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List


@dataclass
class Verse:
    """Represents a single Quran verse (ayah) with all associated data."""

    surah: int
    ayah: int
    arabic_uthmani: str
    arabic_simple: str = ""
    arabic_tajweed: str = ""
    translation: str = ""
    transliteration: str = ""
    audio_url: str = ""
    audio_urls: Dict[str, str] = field(default_factory=dict)
    tafsir: str = ""
    word_by_word: List[Dict[str, Any]] = field(default_factory=list)

    # Metadata
    juz: int = 0
    hizb: int = 0
    hizb_quarter: int = 0
    ruku: int = 0
    manzil: int = 0
    page: int = 0
    sajda: bool = False
    sajda_type: str = ""

    @property
    def reference(self) -> str:
        """Return verse reference in surah:ayah format."""
        return f"{self.surah}:{self.ayah}"

    @property
    def verse_key(self) -> str:
        """Return verse key in surah:ayah format."""
        return f"{self.surah}:{self.ayah}"

    def to_dict(self) -> Dict[str, Any]:
        """Convert verse to dictionary."""
        data = asdict(self)
        data["reference"] = self.reference
        data["verse_key"] = self.verse_key
        return data

    def to_json(self) -> str:
        """Convert verse to JSON string."""
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Verse":
        """Create a Verse instance from a dictionary."""
        # Remove computed properties that aren't constructor args
        filtered = {k: v for k, v in data.items() if k in cls.__dataclass_fields__}
        return cls(**filtered)
