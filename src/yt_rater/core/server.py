from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime

from yt_rater.models.rating_request import RatingRequest
from yt_rater.models.rating_response import RatingResponse
from yt_rater.core.cache import Cache
from yt_rater.core.config import Config
from yt_rater.core.youtube import YoutubeClient
from yt_rater.core.gemini import GeminiClient
from yt_rater.core.exceptions import InvalidURLException, NoCommentFound

config = Config()

class Server:
    def __init__(self, port: int = config.get("server", "port")):
        self.port = port
        print (self.port)
        self.app = FastAPI(title="YT Rater API")
        self.config = Config()
        self.cache = Cache()
        self.youtube = YoutubeClient()
        self.gemini = GeminiClient()

        self._setup_routes()
        self._setup_cors()

    def _setup_cors(self):
        """Allow front-end to access local API."""
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    def _setup_routes(self):
        @self.app.post("/rate", response_model=RatingResponse)
        async def rate_video(request: RatingRequest):
            url = str(request.url)

            # check cache
            score = self.cache.get(url)
            if score is not None:
                return RatingResponse(score=score, last_updated=datetime.now())

            try:
                # extract video ID
                video_id = self.youtube.get_video_id(url)

                # fetch comments
                comments = self.youtube.fetch_comments(
                    video_id, max_comments=config.get("youtube", "max_comments_per_video")
                )
                if not comments:
                    raise NoCommentFound

                # get gemini rating
                score = self.gemini.rate_comments(comments)

                # save in cache
                self.cache.set(url, score)

                return RatingResponse(score=score, last_updated=datetime.now())
            except InvalidURLException as e:
                raise HTTPException(status_code=403, detail=f"403 Forbidden {e}")
            except NoCommentFound as e:
                raise HTTPException(status_code=404, detail=f"No Comment Found!")
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")

    def run(self):
        import uvicorn
        uvicorn.run(self.app, host="0.0.0.0", port=self.port)
