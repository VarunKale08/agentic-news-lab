# Agentic News Lab – Multi-Agent News Dashboard

A multi-agent system for real-time news summarization and sentiment analysis, powered by [CrewAI](https://docs.crewai.com).  
The backend orchestrates AI agents to fetch, clean, summarize, and analyze sentiment of the latest news.  
The frontend dashboard provides a simple interface for searching and visualizing results.

---

## Features
- **Fetcher Agent**: Retrieves latest 15–20 news articles for a given topic.  
- **Cleaner Agent**: Deduplicates, sorts, and formats results.  
- **Summarizer Agent**: Generates strict 2-line summaries.  
- **Sentiment Agent**: Classifies sentiment (Positive, Neutral, Negative).  
- **Manager Agent**: Orchestrates agent workflow.  
- **Optional Knowledge Agent**: RAG with Chroma or Pinecone.   

---

## Project Structure
```
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
```

---

## Setup

### Backend
```bash
cd backend/news_crew

# Activate CrewAI virtual environment
.venv\Scripts\activate    # Windows (PowerShell)
source .venv/bin/activate # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Run backend
python src/news_crew/main.py
```

### Environment variables (.env)
```
GEMINI_API_KEY=your_key
SERPER_API_KEY=your_key
GNEWS_API_KEY=your_key
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

Default frontend: [http://localhost:5173](http://localhost:5173)

---

## Tech Stack
- **Backend**: Python, CrewAI, FastAPI  
- **Frontend**: React + Vite  
- **AI Models**: OpenAI API  
- **Vector DB**: ChromaDB (optional: Pinecone, Google Vector DB)  
- **News APIs**: Serper.dev, GNews  

---

## Contributing
Contributions are welcome!  

1. Fork the repository  
2. Create a new feature branch:
   ```bash
   git checkout -b feature-name
   ```
3. Commit your changes:
   ```bash
   git commit -m "feat: add new feature"
   ```
4. Push to your branch:
   ```bash
   git push origin feature-name
   ```
5. Open a Pull Request  

---

## References
- [CrewAI Docs](https://docs.crewai.com)  
- [Serper.dev](https://serper.dev)  
- [OpenAI API](https://platform.openai.com/docs)  
- [ChromaDB](https://docs.trychroma.com)  
