# yt_rater/core/config.py
import tomllib
import tomli_w
from typing import Any, Dict
from yt_rater.core.constants import Constants

class Config:
    CONFIG_DIR = Constants.DEFAULT_DIR
    CONFIG_FILE = Constants.DEFAULT_CONFIG_FILE

    def __init__(self) -> None:
        self._config: Dict[str, Any] = {}
        self._ensure_config_file()
        self.load()

    def _ensure_config_file(self) -> None:
        """Create the folder + the config file if it does not exist."""
        if not self.CONFIG_DIR.exists():
            self.CONFIG_DIR.mkdir(parents=True)
        if not self.CONFIG_FILE.exists():
            self.save(Constants.DEFAULT_CONFIG)

    def load(self) -> None:
        """Load config from TOML file."""
        with open(self.CONFIG_FILE, "rb") as f:
            self._config = tomllib.load(f)

    def save(self, config: Dict[str, Any] | None = None) -> None:
        """Save config in TOML file."""
        if config is not None:
            self._config = config
        with open(self.CONFIG_FILE, "wb") as f:
            tomli_w.dump(self._config, f)

    def get(self, section: str, key: str, default=None) -> Any:
        if section not in self._config:
            return default
        return self._config[section].get(key, default)

    def set(self, section: str, key: str, value: Any) -> None:
        if section not in self._config:
            self._config[section] = {}
        self._config[section][key] = value
        self.save(self._config)

    @property
    def data(self) -> Dict[str, Any]:
        return self._config
