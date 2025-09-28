# yt_rater/core/constants.py
from pathlib import Path
from typing import Any, Dict

class Constants:
    DEFAULT_FOLDER_NAME = ".yt_rater"
    DEFAULT_CONFIG_FILE_NAME = "config.toml"
    DEFAULT_CACHE_FILE_NAME = "cache.json"
    DEFAULT_CACHE_EXPIRATION_DAYS = 7
    DEFAULT_INDENT = 4
    DEFAULT_SERVER_PORT = 8888
    DEFAULT_MAX_COMMENTS_PER_VIDEO = 50
    DEFAULT_DIR = Path.home() / DEFAULT_FOLDER_NAME
    DEFAULT_CONFIG_FILE = DEFAULT_DIR / DEFAULT_CONFIG_FILE_NAME
    DEFAULT_CACHE_FILE = DEFAULT_DIR / DEFAULT_CACHE_FILE_NAME

    DEFAULT_CONFIG: Dict[str, Any] = {
        "youtube": {
            "api_key": "",
            "max_comments_per_video": DEFAULT_MAX_COMMENTS_PER_VIDEO,
        },
        "gemini": {
            "api_key": "",
            "model": "gemini-2.5-flash-lite",
        },
        "cache": {
            "expiration_days": DEFAULT_CACHE_EXPIRATION_DAYS,
        },
        "server": {
            "port": DEFAULT_SERVER_PORT
        }
    }
