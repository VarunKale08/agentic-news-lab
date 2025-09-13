import json
from crewai.tools import BaseTool
from pydantic import BaseModel, Field, PrivateAttr
from typing import Type
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

# Ensure VADER lexicon is available
try:
    nltk.data.find("sentiment/vader_lexicon.zip")
except LookupError:
    nltk.download("vader_lexicon")


class VaderInput(BaseModel):
    summary: str = Field(..., description="Summary text to classify sentiment")


class VaderSentimentTool(BaseTool):
    name: str = "VADER Sentiment Tool"
    description: str = (
        "Classify sentiment (positive, neutral, negative) using NLTK VADER"
    )
    args_schema: Type[BaseModel] = VaderInput

    # Declare as private attr so Pydantic ignores it
    _analyzer: SentimentIntensityAnalyzer = PrivateAttr()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._analyzer = SentimentIntensityAnalyzer()

    def _run(self, summary: str) -> dict:
        scores = self._analyzer.polarity_scores(summary)
        compound = scores["compound"]

        if compound >= 0.05:
            sentiment = "positive"
        elif compound <= -0.05:
            sentiment = "negative"
        else:
            sentiment = "neutral"

        return {
            "sentiment": sentiment,
            "confidence": round(abs(compound), 2),
        }
