# yt_rater/models/rating_response.py
from pydantic import BaseModel, Field
from datetime import datetime

class RatingResponse(BaseModel):
    score: float = Field(default=0.0, ge=0.0, le=5.0)
    last_updated: datetime
