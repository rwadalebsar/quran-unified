"""Base HTTP client for all API clients."""

import logging
from typing import Any, Dict, Optional

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from quran_unified.exceptions import (
    APIConnectionError,
    NotFoundError,
    QuranAPIError,
    RateLimitError,
)

logger = logging.getLogger(__name__)


class BaseClient:
    """Base client with shared HTTP logic, retries, and session management."""

    BASE_URL: str = ""

    def __init__(self, timeout: int = 30, retries: int = 3):
        self.timeout = timeout
        self.session = requests.Session()

        retry_strategy = Retry(
            total=retries,
            backoff_factor=0.5,
            status_forcelist=[500, 502, 503, 504],
            allowed_methods=["GET"],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("https://", adapter)
        self.session.mount("http://", adapter)

    def _get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Any:
        """Make a GET request and return parsed JSON response."""
        url = f"{self.BASE_URL}{endpoint}"
        try:
            response = self.session.get(url, params=params, timeout=self.timeout)
            self._handle_error(response)
            return response.json()
        except requests.ConnectionError as e:
            raise APIConnectionError(f"Failed to connect to {url}: {e}") from e
        except requests.Timeout as e:
            raise APIConnectionError(f"Request to {url} timed out") from e
        except requests.RequestException as e:
            raise QuranAPIError(f"Request failed: {e}") from e

    def _handle_error(self, response: requests.Response) -> None:
        """Raise appropriate exception for HTTP error responses."""
        if response.status_code == 404:
            raise NotFoundError(f"Resource not found: {response.url}")
        if response.status_code == 429:
            raise RateLimitError("API rate limit exceeded")
        if response.status_code >= 400:
            raise QuranAPIError(
                f"API error {response.status_code}: {response.text[:200]}"
            )

    def close(self) -> None:
        """Close the HTTP session."""
        self.session.close()

    def __enter__(self) -> "BaseClient":
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()
