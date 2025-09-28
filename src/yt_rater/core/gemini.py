from typing import List
import logging

from google import genai
from yt_rater.core.ai import AIClient
from yt_rater.core.exceptions import (
    MissingAIAPIKeyException,
    MissingGeminiAPIKeyException,
)

logger = logging.getLogger(__name__)


class GeminiClient(AIClient):
    """
    Client pour évaluer des commentaires YouTube avec Google Gemini.
    Nécessite un champ "api_key" dans la section "gemini" dans 
    ~/.yt_rater/config.toml et optionnellement "model".
    """

    def __init__(self, api_key: str | None = None, model: str | None = None):
        try:
            super().__init__("gemini", api_key, model)
        except MissingAIAPIKeyException:
            raise MissingGeminiAPIKeyException("Missing ai API KEY. Configure it with 'yt-rater config'.")

        self.client = genai.Client(api_key=self.api_key)

    def rate_comments(self, comments: List[str]) -> float:
        """YouTube video rating based on comments."""
        prompt = self._build_prompt(comments)

        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt
            )
            text = response.text or ""
            score = self._extract_score(text)
            if score:
                return score
            logger.warning("GeminiClient: can't parse output -> return 2.5")
        except Exception as e:
            logger.error(f"GeminiClient error: {e}")

        return 2.5
