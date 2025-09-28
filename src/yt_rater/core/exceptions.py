# yt_rater/core/exceptions.py

from typing import Sequence

class YTRaterException(Exception):
    """Base yt-rater exceptions."""

    def __init__(
            self, msg : str | None = None, stacktrace: Sequence[str] | None = None
    ) -> None:
        super ().__init__ ()
        self.msg = msg
        self.stacktrace = stacktrace

    def __str__ (self) -> str :
        exception_msg = f"Message :{self.msg or ''}\n"
        if self.stacktrace :
            stacktrace = "\n".join (self.stacktrace)
            exception_msg += f"Stacktrace :\n{stacktrace}"
        return exception_msg

class MissingAPIKeyException(YTRaterException):
    """Throw when an API KEY missing."""

class MissingAIAPIKeyException(MissingAPIKeyException):
    """Throw when an AI API KEY missing."""

class MissingGeminiAPIKeyException(MissingAIAPIKeyException):
    """Throw when gemini API Key missing."""

class MissingYouTubeAPIKeyException(MissingAPIKeyException):
    """Throw when YouTube API Key missing."""

class InvalidURLException(YTRaterException):
    """Throw when an URL isn't from YouTube."""

class NoCommentFound(YTRaterException):
    """Throw when YouTube video hasn't comment."""
