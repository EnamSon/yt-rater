# yt_rater/cli.py
import typer
from yt_rater.core.config import Config
from yt_rater.core.server import Server
from yt_rater.core.constants import Constants

app = typer.Typer(help="YT Rater CLI")
app_config = Config()

@app.command()
def config(show: bool = typer.Option(False, "--show", "-s", help="Show current config.")):
    """Get config file (~/.yt_rater/config.json)."""
    cfg = Config()
    if show:
        typer.echo(cfg.CONFIG_FILE.read_text())
    else:
        typer.echo(cfg.CONFIG_FILE)

@app.command()
def run(port: int = typer.Option(app_config.get("server", "port"), "--port", "-p", help="Server listening port.")):
    """Launch local server."""
    cfg = Config()
    youtube_api_key = cfg.get("youtube", "api_key")
    gemini_api_key = cfg.get("gemini", "api_key")

    if not youtube_api_key or not gemini_api_key:
        typer.secho(
            "Error: YouTube API key or Gemini API key not provide.\n"
            "Execute 'yt-rater config' to get config file and edit it.",
            fg=typer.colors.RED,
            err=True,
        )
        raise typer.Exit(code=1)

    typer.echo(f"http://localhost:{port}")
    server = Server(port=port)
    server.run()

def main():
    app()

if __name__ == "__main__":
    main()
