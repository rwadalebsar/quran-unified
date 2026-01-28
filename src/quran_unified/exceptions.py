"""Custom exceptions for the Quran unified API."""


class QuranAPIError(Exception):
    """Base exception for Quran API errors."""

    pass


class InvalidReferenceError(QuranAPIError):
    """Invalid surah/ayah reference."""

    pass


class APIConnectionError(QuranAPIError):
    """Failed to connect to API."""

    pass


class RateLimitError(QuranAPIError):
    """API rate limit exceeded."""

    pass


class NotFoundError(QuranAPIError):
    """Resource not found."""

    pass


class CacheError(QuranAPIError):
    """Cache operation failed."""

    pass
