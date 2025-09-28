# yt_rater/models/rating_request.py
from pydantic import BaseModel, HttpUrl

class RatingRequest(BaseModel):
    url: HttpUrl
