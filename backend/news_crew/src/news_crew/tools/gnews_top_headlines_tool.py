import os
import requests
from typing import Type
from pydantic import BaseModel, Field
from crewai.tools import BaseTool


class GNewsTopHeadlinesInput(BaseModel):
    query: str = Field(
        ..., description="The topic or keyword to search news articles for"
    )
    category: str = Field(
        "general",
        description="News category (general, world, nation, business, technology, entertainment, sports, science, health)",
    )
    lang: str = Field(
        "en", description="Language code of the articles (e.g., en, fr, es)"
    )
    country: str = Field(
        "us", description="Country code for filtering news (e.g., us, gb, in)"
    )
    max_results: int = Field(20, description="Number of results to fetch (1–100)")


class GNewsTopHeadlinesTool(BaseTool):
    name: str = "GNews Top Headlines Tool"
    description: str = (
        "Fetch top news headlines from the GNews API for a given query/topic. "
        "Always returns real articles (not topic pages) with Headline, Source, URL, and Publish Date."
    )
    args_schema: Type[BaseModel] = GNewsTopHeadlinesInput

    def _run(
        self,
        query: str,
        category: str = "general",
        lang: str = "en",
        country: str = "us",
        max_results: int = 20,
    ) -> str:
        api_key = os.getenv("GNEWS_API_KEY")
        if not api_key:
            return "Error: GNEWS_API_KEY not set in environment variables."

        url = (
            f"https://gnews.io/api/v4/top-headlines?"
            f"q={query}&category={category}&lang={lang}&country={country}&max={max_results}&apikey={api_key}"
        )

        try:
            resp = requests.get(url, timeout=10)
            resp.raise_for_status()
            data = resp.json()
            articles = data.get("articles", [])

            if not articles:
                return f"No top headlines found for topic '{query}'."

            results = []
            for art in articles:
                headline = art.get("title", "N/A")
                source = art.get("source", {}).get("name", "Unknown Source")
                link = art.get("url", "N/A")
                published = art.get("publishedAt", "N/A")
                results.append(
                    {
                        "headline": headline,
                        "source": source,
                        "url": link,
                        "publishedAt": published,
                    }
                )

            # Return JSON so agents can easily parse
            return {"topic": query, "articles": results}

        except requests.exceptions.RequestException as e:
            return {"error": f"Error calling GNews API: {e}"}
        except Exception as e:
            return {"error": f"Unexpected error: {e}"}
