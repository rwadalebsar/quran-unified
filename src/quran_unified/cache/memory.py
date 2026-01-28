"""In-memory LRU cache backend."""

import threading
import time
from collections import OrderedDict
from typing import Any, Optional

from quran_unified.cache.base import CacheBackend


class MemoryCache(CacheBackend):
    """In-memory cache with LRU eviction and TTL support."""

    def __init__(self, max_size: int = 1000):
        self._max_size = max_size
        self._cache: OrderedDict[str, Any] = OrderedDict()
        self._expiry: dict[str, float] = {}
        self._lock = threading.Lock()

    def get(self, key: str) -> Optional[Any]:
        with self._lock:
            if key not in self._cache:
                return None
            if key in self._expiry and time.monotonic() > self._expiry[key]:
                del self._cache[key]
                del self._expiry[key]
                return None
            self._cache.move_to_end(key)
            return self._cache[key]

    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        with self._lock:
            if key in self._cache:
                self._cache.move_to_end(key)
            self._cache[key] = value
            if ttl is not None:
                self._expiry[key] = time.monotonic() + ttl
            elif key in self._expiry:
                del self._expiry[key]
            while len(self._cache) > self._max_size:
                oldest_key, _ = self._cache.popitem(last=False)
                self._expiry.pop(oldest_key, None)

    def delete(self, key: str) -> None:
        with self._lock:
            self._cache.pop(key, None)
            self._expiry.pop(key, None)

    def clear(self) -> None:
        with self._lock:
            self._cache.clear()
            self._expiry.clear()
