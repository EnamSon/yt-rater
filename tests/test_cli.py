# tests/test_cli.py
import tomllib
import tomli_w
import pytest
from typer.testing import CliRunner
from yt_rater.cli import app
from yt_rater.core.config import Config
from yt_rater.core.constants import Constants
from yt_rater.core.server import Server

runner = CliRunner()

@pytest.fixture
def temp_config_dir(tmp_path, monkeypatch):
    """Redirects the Config to a temporary folder so as not to touch ~/.yt_rater."""
    monkeypatch.setattr(Config, "CONFIG_DIR", tmp_path)
    monkeypatch.setattr(Config, "CONFIG_FILE", tmp_path / Constants.DEFAULT_CONFIG_FILE_NAME)
    monkeypatch.setattr(Config, "CONFIG_FILE", tmp_path / Constants.DEFAULT_CACHE_FILE_NAME)
    yield tmp_path

def test_config_command_creation(temp_config_dir):
    """Test that the 'config' command creates a config file."""
    result = runner.invoke(app, ["config"])
    assert result.exit_code == 0
    cfg_file = Config.CONFIG_FILE
    assert cfg_file.exists()
    data = tomllib.loads(cfg_file.read_text())
    assert "youtube" in data
    assert "gemini" in data
    assert "cache" in data
    assert "server" in data

def test_config_command_show(temp_config_dir):
    """Test that the 'config --show' command show the content of config file."""
    Config()
    result = runner.invoke(app, ["config", "--show"])
    assert result.exit_code == 0
    output = result.output
    assert "youtube" in output
    assert "gemini" in output
    assert "cache" in output
    assert "server" in output

def test_run_command(temp_config_dir, monkeypatch):
    """Test that the 'run' command call Server.run() (mocked)."""
    called = {}

    def mock_run(self):
        called["yes"] = True

    monkeypatch.setattr(Server, "run", mock_run)
    result = runner.invoke(app, ["run", "--port", "1234"])
    assert result.exit_code == 1
    assert called.get("yes") is not True

    cfg = Config()
    cfg.set("youtube", "api_key", "FAKE_YOUTUBE_API_KEY")
    cfg.set("gemini", "api_key", "FAKE_GEMINI_API_KEY")

    monkeypatch.setattr(Server, "run", mock_run)
    result = runner.invoke(app, ["run", "--port", "1234"])
    assert result.exit_code == 0
    assert called.get("yes") is True
