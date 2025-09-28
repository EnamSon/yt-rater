import pytest
from yt_rater.core.youtube import YoutubeClient
from yt_rater.core.config import Config
from yt_rater.core.constants import Constants
from yt_rater.core.exceptions import InvalidURLException

@pytest.fixture
def fake_config(tmp_path, monkeypatch):
    monkeypatch.setattr(Config, "CONFIG_DIR", tmp_path)
    monkeypatch.setattr(Config, "CONFIG_FILE", tmp_path / Constants.DEFAULT_CONFIG_FILE_NAME)
    cfg = Config()
    cfg.set("youtube", "api_key", "FAKE_KEY")
    return cfg


def test_get_video_id_standard_url(fake_config):
    yt = YoutubeClient(api_key="FAKE_KEY")
    url = "https://www.youtube.com/watch?v=abcd1234"
    assert yt.get_video_id(url) == "abcd1234"


def test_get_video_id_short_url(fake_config):
    yt = YoutubeClient(api_key="FAKE_KEY")
    url = "https://youtu.be/abcd1234"
    assert yt.get_video_id(url) == "abcd1234"


def test_get_video_id_invalid(fake_config):
    yt = YoutubeClient(api_key="FAKE_KEY")
    with pytest.raises(InvalidURLException):
        yt.get_video_id("https://example.com/video")


def test_fetch_comments(monkeypatch, fake_config):
    class FakeRequest:
        def __init__(self, items, next_page=None):
            self._items = items
            self._next_page = next_page
            self._called = False

        def execute(self):
            if not self._called:
                self._called = True
                return {"items": self._items, "nextPageToken": self._next_page}
            return {"items": []} 

    class FakeCommentThreads:
        def __init__(self, responses):
            self._responses = responses
            self._index = 0

        def list(self, **kwargs):
            resp = self._responses[self._index]
            self._index += 1
            return resp

    class FakeYouTube:
        def __init__(self, responses):
            self._commentThreads = FakeCommentThreads(responses)

        def commentThreads(self):
            return self._commentThreads

    response_page1 = FakeRequest(
        items=[{"snippet": {"topLevelComment": {"snippet": {"textDisplay": "Comment 1"}}}}],
        next_page="PAGE2"
    )
    response_page2 = FakeRequest(
        items=[{"snippet": {"topLevelComment": {"snippet": {"textDisplay": "Comment 2"}}}}],
        next_page=None
    )

    def fake_build(service_name, version, developerKey=None):
        assert service_name == "youtube"
        assert version == "v3"
        assert developerKey == "FAKE_KEY"
        return FakeYouTube([response_page1, response_page2])

    monkeypatch.setattr("yt_rater.core.youtube.build", fake_build)

    yt = YoutubeClient(api_key="FAKE_KEY")
    comments = yt.fetch_comments("abcd1234", max_comments=5)
    assert comments == ["Comment 1", "Comment 2"]
