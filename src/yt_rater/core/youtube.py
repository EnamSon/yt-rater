# yt_rater/core/youtube
from typing import List
from urllib.parse import urlparse, parse_qs
from googleapiclient.discovery import build # type: ignore
from yt_rater.core.config import Config
from yt_rater.core.exceptions import (
    InvalidURLException,
    MissingYouTubeAPIKeyException,
)
config = Config()

class YoutubeClient:
    def __init__(self, api_key: str | None = None):
        self._cfg = Config()
        self.api_key = api_key or self._cfg.get("youtube", "api_key")
        if not self.api_key:
            raise MissingYouTubeAPIKeyException(
                "Missing YouTube API KEY. Configure it with 'yt-rater config'"
            )
        self.youtube = build("youtube", "v3", developerKey=self.api_key)

    def get_video_id(self, url: str) -> str:
        """Extract the video ID from YouTube URL."""
        parsed = urlparse(url)
        hostname = parsed.hostname or ""
        if hostname in ["www.youtube.com", "youtube.com"] and parsed.path == "/watch":
            qs = parse_qs(parsed.query)
            vid = qs.get("v", [None])[0]
            if vid:
                return vid
        elif hostname == "youtu.be":
            return parsed.path.lstrip("/")
        raise InvalidURLException(f"Invalid URL: {url}")

    def fetch_comments(
        self, video_id: str, max_comments: int = config.get("youtube", "max_comments_per_video")
    ) -> List[str]:
        """Fetch up to max_comments comments for a YouTube video."""
        comments: List[str] = []
        page_token = None
        max_comments = min(max_comments, self._cfg.get("youtube", "max_comments_per_video"))

        while len(comments) < max_comments:
            request = self.youtube.commentThreads().list(
                part="snippet",
                videoId=video_id,
                textFormat="plainText",
                maxResults=max_comments - len(comments),
                pageToken=page_token,
            )
            response = request.execute()

            for item in response.get("items", []):
                snippet = item["snippet"]["topLevelComment"]["snippet"]
                comments.append(snippet.get("textDisplay", ""))
                if len(comments) >= max_comments:
                    break

            page_token = response.get("nextPageToken")
            if not page_token:
                break

        return comments
