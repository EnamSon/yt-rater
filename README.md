Millions of YouTube videos are uploaded daily. As users of this platform, we sometimes start
watching a video only to realize later that it wasn’t what we expected or the quality was poor.  
For this reason, we use AI to build a tool that ingests comments from a given YouTube video
and tells us how good this video is likely to be before we watch it.

# YT Rater

**YT Rater** is a web extension + local backend that automatically evaluates YouTube videos
based on their comments.  
The local server queries the YouTube API to fetch comments, then calls **Google Gemini**
to generate a score between **0.0 and 5.0**.  
This score is returned to the extension and displayed directly on the video (star rating).

---

## Work in Progress

This repository contains work-in-progress code and is not production-ready.
Use at your own risk, and expect frequent change.

## Features

- Fetches comments from a YouTube video using the official API  
- Analysis and scoring with Google Gemini (`google-genai`)  
- Local cache (avoids re-evaluation of recent videos)  
- Simple configuration stored in `~/.yt_rater/config.toml`  
- CLI (`yt-rater`) with two commands:  
  - `config` → create/show configuration  
  - `run` → start the local FastAPI server  

---

## Installation

### Prerequisites
- Python **3.12+**
- [Poetry](https://python-poetry.org/)

```bash
git clone https://github.com/EnamSon/yt-rater.git
cd yt-rater
poetry install
```

---

## Configuration
Get the configuration file:

```bash
poetry run yt-rater config
```

You need to enable YouTube Data API v3 in your Google Cloud project
and obtain an API key.
For Gemini, create a key from your Google AI Studio or Vertex AI account.

---

## Run the server

```bash
poetry run yt-rater run --port 8800
```

The server runs at http://localhost:8800
Available endpoint:
- POST /rate: receives { "url": "<video_url>" } and returns { "score": 4.2, "last_updated": "..." }

```bash
curl -X POST http://localhost:8800/rate \
     -H "Content-Type: application/json" \
     -d '{"url":"https://www.youtube.com/watch?v=dQw4w9WgXcQ"}'
```

---

## Tests

Run the full test suite:

```bash
poetry run pytest
```

The tests use pytest and mock YouTube/Gemini calls, so they don’t consume real API quota.

---

## Developement

Projet structure:

```
yt-rater/
│
├── pyproject.toml               # Managed by Poetry
├── README.md
├── .gitignore
│
├── src/yt_rater/                # Main package
│   ├── __init__.py
│   ├── cli.py                   # CLI entry point (Typer)
│   │
│   ├── core/                    # Core logic (OOP)
│   │   ├── __init__.py
│   │   ├── server.py            # Server class (FastAPI wrapper)
│   │   ├── config.py            # Config class (handles config.json)
│   │   ├── cache.py             # Cache class (memory + persistence)
│   │   ├── youtube.py           # YoutubeClient (google-api-python-client)
│   │   └── gemini.py            # GeminiClient (google-genai)
│   │
│   └── models/                  # Business models (Pydantic)
│       ├── __init__.py
│       ├── rating_request.py    # {url: str}
│       └── rating_response.py   # {score: float, last_updated: datetime}
│
└── tests/                       # Unit/integration tests
    ├── __init__.py
    ├── test_cli.py
    ├── test_config.py
    ├── test_cache.py
    ├── test_server.py
    └── test_youtube.py
```
---

## TODO

- Integration with a browser extension (overlay on YouTube videos)
- Support other AI API
- Bug correction
- Tests improvement
- Code improvement

## License

This project is licensed under the MIT License.
