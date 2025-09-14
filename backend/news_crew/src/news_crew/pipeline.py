# import json
# from news_crew.crew import NewsCrew

# def run_news_pipeline(topic: str):
#     """Run the NewsCrew pipeline dynamically with a given topic and clean JSON output"""
#     try:
#         raw_result = NewsCrew().crew().kickoff(inputs={"topic": topic})

#         articles = []
#         sentiment_distribution = {"Positive": 0, "Neutral": 0, "Negative": 0}

#         # Case 1: Raw result is already dict-like
#         if isinstance(raw_result, dict):
#             articles = raw_result.get("articles", [])

#         # Case 2: Raw result is a string containing JSON in backticks
#         elif isinstance(raw_result, str):
#             cleaned = raw_result.strip("` \n")
#             if cleaned.startswith("json"):
#                 cleaned = cleaned[4:].strip()  # remove "json" marker
#             try:
#                 articles = json.loads(cleaned)
#             except Exception:
#                 articles = [{"headline": cleaned, "summary": cleaned}]

#         # Case 3: Raw result is a list of dicts
#         elif isinstance(raw_result, list):
#             articles = raw_result

#         # Build sentiment distribution
#         for article in articles:
#             sentiment = str(article.get("sentiment", "Neutral")).capitalize()
#             if sentiment in sentiment_distribution:
#                 sentiment_distribution[sentiment] += 1
#             else:
#                 sentiment_distribution["Neutral"] += 1

#         # Normalize articles: only keep the fields frontend needs
#         cleaned_articles = []
#         for article in articles:
#             cleaned_articles.append({
#                 "headline": article.get("headline", ""),
#                 "summary": article.get("summary", ""),
#                 "sentiment": str(article.get("sentiment", "Neutral")).capitalize(),
#                 "source": article.get("source", ""),
#                 "url": article.get("url", ""),
#                 "publish_date": article.get("publish_date", ""),
#             })

#         return {
#             "topic": topic,
#             "articles": cleaned_articles,
#             "sentiment_distribution": sentiment_distribution,
#         }

#     except Exception as e:
#         return {
#             "topic": topic,
#             "articles": [],
#             "sentiment_distribution": {"Positive": 0, "Neutral": 0, "Negative": 0},
#             "error": str(e),
#         }
import json
import re
from typing import Any, List, Dict, Optional
from news_crew.crew import NewsCrew


def _strip_code_fences(s: str) -> str:
    # Remove ```json ... ``` or ``` ... ``` fences
    s = s.strip()
    s = re.sub(r"^\s*```[a-zA-Z]*\s*\n", "", s, flags=re.IGNORECASE)
    s = re.sub(r"\n?\s*```$", "", s)
    return s.strip()


def _try_parse_jsonish(text: str) -> Optional[List[Dict[str, Any]]]:
    text = _strip_code_fences(text)
    try:
        data = json.loads(text)
        if isinstance(data, list):
            return data
        if (
            isinstance(data, dict)
            and "articles" in data
            and isinstance(data["articles"], list)
        ):
            return data["articles"]
    except Exception:
        pass
    return None


def _from_output_object(output: Any, crew_obj: Any = None) -> List[Dict[str, Any]]:
    """
    Try to extract articles from various possible CrewAI return shapes.
    1) list[dict] or dict{'articles': ...}
    2) CrewOutput.json_dict / .raw / .pydantic
    3) crew.output.{json_dict, raw, pydantic}
    4) str(output)
    """
    # Direct types first
    if isinstance(output, list):
        return output
    if isinstance(output, dict):
        if "articles" in output and isinstance(output["articles"], list):
            return output["articles"]
        # Otherwise, maybe the dict itself is the list structure; ignore.

    # Try CrewOutput-like attributes on the returned object
    for obj in [output, getattr(crew_obj, "output", None)]:
        if obj is None:
            continue
        # JSON dict (only present if you configured output_json/output_pydantic)
        jd = getattr(obj, "json_dict", None)
        if jd:
            if isinstance(jd, list):
                return jd
            if isinstance(jd, dict) and isinstance(jd.get("articles"), list):
                return jd["articles"]
        # Raw text
        raw = getattr(obj, "raw", None)
        if isinstance(raw, str):
            parsed = _try_parse_jsonish(raw)
            if parsed is not None:
                return parsed
        # Pydantic model
        p = getattr(obj, "pydantic", None)
        if p is not None:
            try:
                data = p.model_dump() if hasattr(p, "model_dump") else p.dict()
                if isinstance(data, list):
                    return data
                if isinstance(data, dict) and isinstance(data.get("articles"), list):
                    return data["articles"]
            except Exception:
                pass

    # Fallback: string representation
    try:
        as_text = str(output)
        parsed = _try_parse_jsonish(as_text)
        if parsed is not None:
            return parsed
    except Exception:
        pass

    return []


def run_news_pipeline(topic: str):
    """Run NewsCrew and return clean JSON for the frontend."""
    try:
        crew = NewsCrew().crew()
        result = crew.kickoff(inputs={"topic": topic})

        # Robustly extract the list of article dicts
        articles_raw = _from_output_object(result, crew_obj=crew)

        # Build sentiment distribution + normalize fields
        sentiment_counts = {"Positive": 0, "Neutral": 0, "Negative": 0}
        cleaned_articles: List[Dict[str, Any]] = []
        for a in articles_raw:
            sentiment = str(a.get("sentiment", "Neutral")).capitalize()
            if sentiment not in sentiment_counts:
                sentiment = "Neutral"
            sentiment_counts[sentiment] += 1

            cleaned_articles.append(
                {
                    "headline": a.get("headline", ""),
                    "summary": a.get("summary", ""),
                    "sentiment": sentiment,
                    "source": a.get("source", ""),
                    "url": a.get("url", ""),
                    "publish_date": a.get("publish_date", ""),
                    # keep confidence if you want to use it later:
                    # "confidence": a.get("confidence")
                }
            )

        return {
            "topic": topic,
            "articles": cleaned_articles,
            "sentiment_distribution": sentiment_counts,
        }

    except Exception as e:
        return {
            "topic": topic,
            "articles": [],
            "sentiment_distribution": {"Positive": 0, "Neutral": 0, "Negative": 0},
            "error": str(e),
        }
