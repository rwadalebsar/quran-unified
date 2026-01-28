"""Abstract base class for cache backends."""

from abc import ABC, abstractmethod
from typing import Any, Optional


class CacheBackend(ABC):
    """Abstract cache interface."""

    @abstractmethod
    def get(self, key: str) -> Optional[Any]:
        """Retrieve a value by key. Returns None if not found or expired."""
        ...

    @abstractmethod
    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """Store a value with an optional TTL in seconds."""
        ...

    @abstractmethod
    def delete(self, key: str) -> None:
        """Delete a key from the cache."""
        ...

    @abstractmethod
    def clear(self) -> None:
        """Remove all entries from the cache."""
        ...


class NoCache(CacheBackend):
    """Cache backend that does nothing (caching disabled)."""

    def get(self, key: str) -> Optional[Any]:
        return None

    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        pass

    def delete(self, key: str) -> None:
        pass

    def clear(self) -> None:
        pass
