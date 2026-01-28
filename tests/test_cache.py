"""Tests for cache backends."""

import tempfile
import time

import pytest

from quran_unified.cache import MemoryCache, NoCache, SQLiteCache


class TestMemoryCache:
    """Tests for the MemoryCache backend."""

    def test_set_and_get(self, memory_cache):
        memory_cache.set("key1", {"data": "value"})
        result = memory_cache.get("key1")
        assert result == {"data": "value"}

    def test_get_missing_key(self, memory_cache):
        result = memory_cache.get("nonexistent")
        assert result is None

    def test_delete(self, memory_cache):
        memory_cache.set("key1", "value")
        memory_cache.delete("key1")
        assert memory_cache.get("key1") is None

    def test_clear(self, memory_cache):
        memory_cache.set("key1", "value1")
        memory_cache.set("key2", "value2")
        memory_cache.clear()
        assert memory_cache.get("key1") is None
        assert memory_cache.get("key2") is None

    def test_ttl_expiration(self):
        cache = MemoryCache()
        cache.set("key1", "value", ttl=1)
        assert cache.get("key1") == "value"
        time.sleep(1.1)
        assert cache.get("key1") is None

    def test_lru_eviction(self):
        cache = MemoryCache(max_size=3)
        cache.set("key1", "value1")
        cache.set("key2", "value2")
        cache.set("key3", "value3")
        cache.set("key4", "value4")  # Should evict key1
        assert cache.get("key1") is None
        assert cache.get("key2") == "value2"

    def test_lru_access_updates_order(self):
        cache = MemoryCache(max_size=3)
        cache.set("key1", "value1")
        cache.set("key2", "value2")
        cache.set("key3", "value3")
        cache.get("key1")  # Access key1, making it most recent
        cache.set("key4", "value4")  # Should evict key2
        assert cache.get("key1") == "value1"
        assert cache.get("key2") is None


class TestNoCache:
    """Tests for the NoCache backend."""

    def test_set_does_nothing(self, no_cache):
        no_cache.set("key", "value")
        assert no_cache.get("key") is None

    def test_get_returns_none(self, no_cache):
        assert no_cache.get("anything") is None

    def test_delete_does_nothing(self, no_cache):
        no_cache.delete("key")  # Should not raise

    def test_clear_does_nothing(self, no_cache):
        no_cache.clear()  # Should not raise


class TestSQLiteCache:
    """Tests for the SQLiteCache backend."""

    @pytest.fixture
    def sqlite_cache(self):
        with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
            cache = SQLiteCache(db_path=f.name)
            yield cache
            cache.close()

    def test_set_and_get(self, sqlite_cache):
        sqlite_cache.set("key1", {"data": "value"})
        result = sqlite_cache.get("key1")
        assert result == {"data": "value"}

    def test_get_missing_key(self, sqlite_cache):
        result = sqlite_cache.get("nonexistent")
        assert result is None

    def test_delete(self, sqlite_cache):
        sqlite_cache.set("key1", "value")
        sqlite_cache.delete("key1")
        assert sqlite_cache.get("key1") is None

    def test_clear(self, sqlite_cache):
        sqlite_cache.set("key1", "value1")
        sqlite_cache.set("key2", "value2")
        sqlite_cache.clear()
        assert sqlite_cache.get("key1") is None
        assert sqlite_cache.get("key2") is None

    def test_ttl_expiration(self, sqlite_cache):
        sqlite_cache.set("key1", "value", ttl=1)
        assert sqlite_cache.get("key1") == "value"
        time.sleep(1.1)
        assert sqlite_cache.get("key1") is None

    def test_replace_existing_key(self, sqlite_cache):
        sqlite_cache.set("key1", "value1")
        sqlite_cache.set("key1", "value2")
        assert sqlite_cache.get("key1") == "value2"
