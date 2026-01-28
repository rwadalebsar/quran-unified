"""Reciter data model."""

from dataclasses import asdict, dataclass
from enum import Enum
from typing import Any, Dict


class RecitationStyle(Enum):
    """Style of Quran recitation."""

    MURATTAL = "Murattal"
    MUJAWWAD = "Mujawwad"
    MUALLIM = "Muallim"


@dataclass
class Reciter:
    """Represents a Quran reciter."""

    id: str
    name_arabic: str
    name_english: str
    style: RecitationStyle
    bitrate: int = 128

    def to_dict(self) -> Dict[str, Any]:
        """Convert reciter to dictionary."""
        data = asdict(self)
        data["style"] = self.style.value
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Reciter":
        """Create a Reciter instance from a dictionary."""
        data = dict(data)
        if "style" in data and isinstance(data["style"], str):
            data["style"] = RecitationStyle(data["style"])
        filtered = {k: v for k, v in data.items() if k in cls.__dataclass_fields__}
        return cls(**filtered)
