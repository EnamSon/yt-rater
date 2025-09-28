# yt_rater/core/ai.py
from typing import List
import json
import re
import logging

from google import genai
from yt_rater.core.config import Config
from yt_rater.core.exceptions import MissingAIAPIKeyException

logger = logging.getLogger(__name__)
config = Config()

class AIClient:
    """Base of GeminiClient and other AI."""
    def __init__(self, ai: str , api_key: str | None = None, model: str | None = None):
        self.ai = ai
        self._cfg = Config()
        self.api_key = api_key or self._cfg.get(ai, "api_key")
        self.model = model or self._cfg.get(ai, "model", default="gemini-2.5-flash-lite")

        if not self.api_key:
            raise MissingAIAPIKeyException(f"Missing ai API KEY. Configure it with 'yt-rater config'.")

        self.client = genai.Client(api_key=self.api_key)

    def _build_prompt(
        self, comments: List[str], max_comments: int = config.get("youtube", "max_comments_per_video")
    ) -> str:
        comments = comments[:max_comments]
        joined = "\n---\n".join(c.replace("\n", " ") for c in comments if c.strip())

        prompt = (
            "Tu es un assistant qui évalue la pertinence globale d'une vidéo YouTube "
            "à partir des commentaires. Retourne UNIQUEMENT un nombre flottant compris "
            "entre 0.0 et 5.0 avec une précision d'au plus deux chiffres après la virgule."
            f"Voici les commentaires :\n{joined}"
        )
        return prompt

    def _extract_score(self, text: str) -> float | None:
        """Extract score from ai response."""
        try:
            match = re.search(r"\d+(\.\d{1,2})?", text)
            if match:
                score = float(match.group(0))
                if isinstance(score, float) and 0.0 <= score <= 5.0:
                    return score
        except Exception:
            pass
        return None
