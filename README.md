Agentic News Lab – Multi-Agent News Dashboard
============================================

A multi-agent system for real-time news summarization and sentiment analysis, powered by CrewAI.
The backend orchestrates AI agents to fetch, clean, summarize, and analyze sentiment of the latest news.
The frontend dashboard provides a simple interface for searching and visualizing results.

---

Features
- Fetcher Agent: Retrieves latest 15–20 news articles for a given topic.
- Cleaner Agent: Deduplicates, sorts, and formats results.
- Summarizer Agent: Generates strict 2-line summaries.
- Sentiment Agent: Classifies sentiment (Positive, Neutral, Negative).
- Manager Agent: Orchestrates agent workflow.
- Optional Knowledge Agent: RAG with Chroma or Pinecone.

---

Project Structure
agentic-news-lab
│
├── backend
│   └── news_crew
│       ├── .venv/               # CrewAI virtual environment
│       ├── knowledge/           # Vector DB storage
│       ├── src/news_crew/
│       │   ├── config/
│       │   │   ├── agents.yaml  # Agent definitions
│       │   │   └── tasks.yaml   # Task definitions
│       │   ├── tools/           # Custom scraping & news tools
│       │   ├── crew.py          # Crew orchestration
│       │   └── main.py          # Backend entrypoint
│       ├── tests/
│       ├── .env                 # API keys & secrets
│       └── requirements.txt     # Backend dependencies
│
└── frontend
    ├── src/components/          # React components
    │   ├── SearchBar.jsx
    │   ├── NewsCard.jsx
    │   └── SentimentChart.jsx
    └── vite.config.js

---

Setup

Backend
cd backend/news_crew
.venv\Scripts\activate    # Windows (PowerShell)
source .venv/bin/activate # Linux/Mac

pip install -r requirements.txt

python src/news_crew/main.py

Environment variables (.env):
OPENAI_API_KEY=your_key
SERPER_API_KEY=your_key

Frontend
cd frontend
npm install
npm run dev

Default: http://localhost:5173

---

Tech Stack
Backend: Python, CrewAI, FastAPI
Frontend: React + Vite
AI Models: OpenAI API
Vector DB: ChromaDB (optional: Pinecone, Google Vector DB)
News API: Serper.dev, GNews

---

References
CrewAI Docs: https://docs.crewai.com
Serper.dev: https://serper.dev
OpenAI API: https://platform.openai.com/docs
ChromaDB: https://docs.trychroma.com
