# tests/test_config.py
import tomllib
import pytest
from pathlib import Path
from yt_rater.core.config import Config
from yt_rater.core.constants import Constants

@pytest.fixture
def temp_config_dir(tmp_path):
    original_dir = Config.CONFIG_DIR
    Config.CONFIG_DIR = tmp_path
    Config.CONFIG_FILE = tmp_path / Constants.DEFAULT_CONFIG_FILE_NAME
    yield tmp_path

    Config.CONFIG_DIR = original_dir
    Config.CONFIG_FILE = original_dir / Constants.DEFAULT_CONFIG_FILE_NAME


def test_config_creation(temp_config_dir):
    cfg = Config()
    assert cfg.CONFIG_FILE.exists()
    data = tomllib.loads(cfg.CONFIG_FILE.read_text())
    assert data == cfg.data


def test_config_get(temp_config_dir):
    cfg = Config()
    assert cfg.data.keys() == Constants.DEFAULT_CONFIG.keys()

    for section, sub_section in cfg.data.items():
        for key, val in sub_section.items():
            assert isinstance(Constants.DEFAULT_CONFIG[section][key], type(val))
            assert cfg.get(section, key) == val


def test_config_set(temp_config_dir):
    cfg = Config()
    cfg.set("cache", "expiration_days", 10)
    assert cfg.get("cache", "expiration_days") == 10
    new_cfg = Config()
    assert new_cfg.data == cfg.data
