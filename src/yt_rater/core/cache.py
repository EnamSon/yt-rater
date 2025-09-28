# yt_rater/core/cache.py
import json
from datetime import datetime, timedelta
from yt_rater.core.config import Config
from yt_rater.core.constants import Constants

class Cache:
    CACHE_FILE = Constants.DEFAULT_CACHE_FILE

    def __init__(self, expiration_days: int | None = None):
        self._config = Config()
        self._expiration_days = (
            expiration_days if expiration_days is not None else self._config.get(
                "cache", "expiration_days", Constants.DEFAULT_CACHE_EXPIRATION_DAYS
            )
        )
        self._data: dict[str, dict] = {}
        self._ensure_cache_file()
        self.load()

    def _ensure_cache_file(self) -> None:
        """Create empty cache file if it not exists."""
        if not self.CACHE_FILE.parent.exists():
            self.CACHE_FILE.parent.mkdir(parents=True)
        if not self.CACHE_FILE.exists():
            self.save()

    def load(self) -> None:
        """Load cache from JSON file."""
        try:
            with open(self.CACHE_FILE, "r", encoding="utf-8") as f:
                self._data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self._data = {}

    def save(self) -> None:
        """Save cache in JSON file."""
        with open(self.CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump(self._data, f, indent=Constants.DEFAULT_INDENT)

    def is_expired(self, url: str) -> bool:
        entry = self._data.get(url)
        if not entry:
            return True
        last_updated = datetime.fromisoformat(entry["last_updated"])
        return datetime.now() - last_updated > timedelta(days=self._expiration_days)

    def get(self, url: str) -> float | None:
        """Return the score of url if it exists and has not expired."""
        if self.is_expired(url):
            return None
        return self._data[url]["score"]

    def set(self, url: str, score: float) -> None:
        self._data[url] = {
            "score": score,
            "last_updated": datetime.now().isoformat()
        }
        self.save()

    @property
    def data(self) -> dict:
        return self._data
