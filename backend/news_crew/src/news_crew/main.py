#!/usr/bin/env python
import sys
import warnings
import asyncio, json
from datetime import datetime

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse

from news_crew.crew import NewsCrew
from news_crew.pipeline import run_news_pipeline  # ✅ clean import, no circular

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# ---------------- FastAPI setup ----------------
app = FastAPI()

# Enable CORS for frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # later restrict to http://localhost:5173
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------- Endpoints ----------------
@app.get("/api/health")
async def health_check():
    return {"status": "ok", "message": "Backend is running with FastAPI + CrewAI"}


@app.get("/api/news")
async def get_news(topic: str):
    """Run CrewAI pipeline with a user-provided topic (blocking)."""
    result = run_news_pipeline(topic)
    return result


@app.get("/api/news-stream")
async def news_stream(topic: str):
    """Stream CrewAI pipeline progress + final JSON result."""

    async def event_generator():
        yield f"data: Starting pipeline for {topic}\n\n"

        # (Optional) fake phases before running
        yield "data: Running Fetcher Agent...\n\n"
        await asyncio.sleep(0.1)
        yield "data: Running Cleaner Agent...\n\n"
        await asyncio.sleep(0.1)
        yield "data: Running Summarizer Agent...\n\n"
        await asyncio.sleep(0.1)
        yield "data: Running Sentiment Agent...\n\n"
        await asyncio.sleep(0.1)

        # Run heavy work in a background thread
        loop = asyncio.get_running_loop()
        work_task = loop.run_in_executor(None, run_news_pipeline, topic)

        # Keep-alive until done
        while not work_task.done():
            yield "data: ⏳ working...\n\n"
            await asyncio.sleep(2)

        result = await work_task
        yield f"data: {json.dumps(result)}\n\n"
        yield "event: end\ndata: done\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")


# ---------------- CLI helpers ----------------
def run():
    """Run crew manually."""
    inputs = {"topic": "Israel"}
    try:
        NewsCrew().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


def train():
    """Train the crew."""
    inputs = {"topic": "AI LLMs", "current_year": str(datetime.now().year)}
    try:
        NewsCrew().crew().train(
            n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs
        )
    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")


def replay():
    """Replay crew execution from a specific task."""
    try:
        NewsCrew().crew().replay(task_id=sys.argv[1])
    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")


def test():
    """Test the crew execution and return results."""
    inputs = {"topic": "AI LLMs", "current_year": str(datetime.now().year)}
    try:
        NewsCrew().crew().test(
            n_iterations=int(sys.argv[1]), eval_llm=sys.argv[2], inputs=inputs
        )
    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")
