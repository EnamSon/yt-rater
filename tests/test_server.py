import pytest
from fastapi.testclient import TestClient
from yt_rater.core.server import Server
from yt_rater.core.exceptions import InvalidURLException

@pytest.fixture
def client(monkeypatch):
    """Make FastAPI client with mocked YoutubeClient and mocked GeminiClient."""

    # Fake YoutubeClient
    class FakeYoutube:
        def get_video_id(self, url: str) -> str:
            return "video123"

        def fetch_comments(self, video_id: str, max_comments: int = 100):
            return ["Great video!", "Not bad", "Could be better"]

    # Fake GeminiClient
    class FakeGemini:
        def rate_comments(self, comments):
            return 4.5

    # Monkeypatch to replace true clients
    monkeypatch.setattr("yt_rater.core.server.YoutubeClient", lambda *a, **k: FakeYoutube())
    monkeypatch.setattr("yt_rater.core.server.GeminiClient", lambda *a, **k: FakeGemini())

    server = Server(port=8001)
    return TestClient(server.app)


def test_rate_success(client):
    response = client.post("/rate", json={"url": "https://www.youtube.com/watch?v=abcd"})
    assert response.status_code == 200
    data = response.json()
    assert "score" in data
    assert data["score"] == 4.5
    assert "last_updated" in data


def test_rate_invalid_url(client, monkeypatch):
    # Monkeypatch to throw a InvalidURLException
    class BadYoutube:
        def get_video_id(self, url: str):
            raise InvalidURLException

        def fetch_comments(self, video_id: str, max_comments: int = 100):
            return []

    monkeypatch.setattr("yt_rater.core.server.YoutubeClient", lambda *a, **k: BadYoutube())

    server = Server(port=8002)
    client_bad = TestClient(server.app)

    response = client_bad.post("/rate", json={"url": "https://notyoutube.com/vid"})
    assert response.status_code == 403


def test_rate_no_comments(client, monkeypatch):
    # Monkeypatch to return an empty list
    class EmptyYoutube:
        def get_video_id(self, url: str):
            return "video123"

        def fetch_comments(self, video_id: str, max_comments: int = 100):
            return []

    monkeypatch.setattr("yt_rater.core.server.YoutubeClient", lambda *a, **k: EmptyYoutube())

    server = Server(port=8003)
    client_empty = TestClient(server.app)

    response = client_empty.post("/rate", json={"url": "https://www.youtube.com/watch?v=abcd"})
    assert response.status_code == 404
