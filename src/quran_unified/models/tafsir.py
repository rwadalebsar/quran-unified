"""Tafsir data model."""

from dataclasses import asdict, dataclass
from typing import Any, Dict


@dataclass
class Tafsir:
    """Represents a Quran tafsir (interpretation/commentary)."""

    id: int
    name: str
    author: str
    language: str
    book_name: str = ""
    text: str = ""

    def to_dict(self) -> Dict[str, Any]:
        """Convert tafsir to dictionary."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Tafsir":
        """Create a Tafsir instance from a dictionary."""
        filtered = {k: v for k, v in data.items() if k in cls.__dataclass_fields__}
        return cls(**filtered)
