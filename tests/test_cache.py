# tests/test_cache.py
import json
import pytest
from pathlib import Path
from datetime import datetime, timedelta
from yt_rater.core.cache import Cache
from yt_rater.core.config import Config
from yt_rater.core.constants import Constants

@pytest.fixture
def temp_cache_dir(tmp_path, monkeypatch):
    monkeypatch.setattr(Cache, "CACHE_FILE", tmp_path / Constants.DEFAULT_CACHE_FILE_NAME)
    yield tmp_path


def test_cache_creation(temp_cache_dir):
    cache = Cache()
    assert cache.CACHE_FILE.exists()
    assert cache.data == {}


def test_cache_get_set(temp_cache_dir):
    """Test get and set methods."""
    cache = Cache(expiration_days=7)

    url = "https://youtube.com/video123"
    score = 4
    assert cache.get(url) is None

    cache.set(url, score)
    assert cache.get(url) == score

    new_cache = Cache(expiration_days=7)
    assert new_cache.get(url) == score


def test_cache_expiration(temp_cache_dir, monkeypatch):
    """Test the entry expiration by simulate a date from two days ago."""
    cache = Cache(expiration_days=1)

    url = "https://youtube.com/video_expire"
    score = 5
    cache.set(url, score)
    assert cache.get(url) == score

    old_date = (datetime.now() - timedelta(days=2)).isoformat()
    cache._data[url]["last_updated"] = old_date
    cache.save()

    new_cache = Cache(expiration_days=1)
    assert new_cache.get(url) is None
