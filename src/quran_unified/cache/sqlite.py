"""SQLite-based persistent cache backend."""

import json
import os
import sqlite3
import time
from typing import Any, Optional

from quran_unified.cache.base import CacheBackend
from quran_unified.exceptions import CacheError


class SQLiteCache(CacheBackend):
    """Persistent cache using a local SQLite database."""

    def __init__(self, db_path: str = "~/.quran_unified/cache.db"):
        self._db_path = os.path.expanduser(db_path)
        os.makedirs(os.path.dirname(self._db_path), exist_ok=True)
        self._conn = sqlite3.connect(self._db_path, check_same_thread=False)
        self._create_table()

    def _create_table(self) -> None:
        try:
            self._conn.execute(
                """
                CREATE TABLE IF NOT EXISTS cache (
                    key TEXT PRIMARY KEY,
                    value TEXT NOT NULL,
                    expires_at REAL
                )
                """
            )
            self._conn.commit()
        except sqlite3.Error as e:
            raise CacheError(f"Failed to initialize cache database: {e}") from e

    def get(self, key: str) -> Optional[Any]:
        try:
            cursor = self._conn.execute(
                "SELECT value, expires_at FROM cache WHERE key = ?", (key,)
            )
            row = cursor.fetchone()
            if row is None:
                return None
            value, expires_at = row
            if expires_at is not None and time.time() > expires_at:
                self.delete(key)
                return None
            return json.loads(value)
        except sqlite3.Error as e:
            raise CacheError(f"Cache read failed: {e}") from e

    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        try:
            expires_at = time.time() + ttl if ttl is not None else None
            self._conn.execute(
                "INSERT OR REPLACE INTO cache (key, value, expires_at) VALUES (?, ?, ?)",
                (key, json.dumps(value, ensure_ascii=False), expires_at),
            )
            self._conn.commit()
        except (sqlite3.Error, TypeError) as e:
            raise CacheError(f"Cache write failed: {e}") from e

    def delete(self, key: str) -> None:
        try:
            self._conn.execute("DELETE FROM cache WHERE key = ?", (key,))
            self._conn.commit()
        except sqlite3.Error as e:
            raise CacheError(f"Cache delete failed: {e}") from e

    def clear(self) -> None:
        try:
            self._conn.execute("DELETE FROM cache")
            self._conn.commit()
        except sqlite3.Error as e:
            raise CacheError(f"Cache clear failed: {e}") from e

    def close(self) -> None:
        """Close the database connection."""
        self._conn.close()
