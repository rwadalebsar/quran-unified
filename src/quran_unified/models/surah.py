"""Surah data model."""

from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Any, Dict, List, Tuple

from quran_unified.models.verse import Verse


class RevelationType(Enum):
    """Type of Quran revelation."""

    MECCAN = "Meccan"
    MEDINAN = "Medinan"


@dataclass
class Surah:
    """Represents a Quran chapter (surah) with metadata."""

    number: int
    name_arabic: str
    name_english: str
    name_transliteration: str
    verses_count: int
    revelation_type: RevelationType
    revelation_order: int
    pages: Tuple[int, int] = (0, 0)
    verses: List[Verse] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """Convert surah to dictionary."""
        data = asdict(self)
        data["revelation_type"] = self.revelation_type.value
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Surah":
        """Create a Surah instance from a dictionary."""
        data = dict(data)
        if "revelation_type" in data and isinstance(data["revelation_type"], str):
            data["revelation_type"] = RevelationType(data["revelation_type"])
        if "pages" in data and isinstance(data["pages"], list):
            data["pages"] = tuple(data["pages"])
        if "verses" in data and data["verses"]:
            data["verses"] = [
                Verse.from_dict(v) if isinstance(v, dict) else v for v in data["verses"]
            ]
        filtered = {k: v for k, v in data.items() if k in cls.__dataclass_fields__}
        return cls(**filtered)
