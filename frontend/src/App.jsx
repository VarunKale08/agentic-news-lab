import { useState } from "react"
import SearchBar from "./components/SearchBar"
import NewsCard from "./components/NewsCard"
import SentimentChart from "./components/SentimentChart"

const API_URL = import.meta.env.VITE_API_URL ?? "http://127.0.0.1:8000"

function App() {
  const [articles, setArticles] = useState([])
  const [sentiment, setSentiment] = useState({})
  const [logs, setLogs] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState("")

  const handleSearch = (topic) => {
    setLoading(true)
    setError("")
    setArticles([])
    setSentiment({})
    setLogs([`🔎 Searching for "${topic}"...`])

    // connect to SSE endpoint
    const es = new EventSource(
      `${API_URL}/api/news-stream?topic=${encodeURIComponent(topic)}`
    )

    es.onmessage = (event) => {
      try {
        // Final result arrives as JSON
        const parsed = JSON.parse(event.data)
        setArticles(parsed.articles || [])
        setSentiment(parsed.sentiment_distribution || {})
        setLogs((prev) => [...prev, "✅ Pipeline complete"])
        setLoading(false)
        es.close()
      } catch {
        // Progress update (plain text)
        setLogs((prev) => [...prev, event.data])
      }
    }

    es.onerror = (err) => {
      console.error("SSE error:", err)
      setError("Stream error. Please try again.")
      setLoading(false)
      es.close()
    }
  }

  return (
    <div className="min-h-screen bg-gray-900 text-white p-6">
      {/* Header */}
      <h1 className="text-3xl font-bold text-center mb-6">
        📰 Multi-Agent News Dashboard
      </h1>

      {/* Search bar */}
      <SearchBar onSearch={handleSearch} />

      {/* Progress logs - only visible while loading */}
      {loading && logs.length > 0 && (
        <div className="mt-6">
          <h2 className="text-lg font-semibold mb-3">Pipeline Progress</h2>
          <div className="bg-gray-800/70 rounded-lg p-6">
            <ul className="relative border-l border-gray-600 space-y-4 pl-4">
              {logs.map((l, i) => {
                const isComplete =
                  l.includes("✅") || l.toLowerCase().includes("complete")
                const isWorking =
                  l.includes("⏳") || l.toLowerCase().includes("running")

                return (
                  <li key={i} className="flex items-start gap-3">
                    {/* Timeline dot */}
                    <span
                      className={`absolute -left-1.5 w-3 h-3 rounded-full ${
                        isComplete
                          ? "bg-green-500"
                          : isWorking
                          ? "bg-blue-500 animate-pulse"
                          : "bg-gray-500"
                      }`}
                    />
                    {/* Log text */}
                    <span
                      className={`ml-4 text-sm ${
                        isComplete
                          ? "text-green-400"
                          : isWorking
                          ? "text-blue-300"
                          : "text-gray-300"
                      }`}
                    >
                      {l}
                    </span>
                  </li>
                )
              })}
            </ul>
          </div>
        </div>
      )}

      {/* Error message */}
      {error && <p className="text-center mt-6 text-red-500">{error}</p>}

      {/* Empty state */}
      {!loading && !error && articles.length === 0 && (
        <p className="text-center mt-6 text-gray-400">
          No articles yet — try searching for a topic.
        </p>
      )}

      {/* Sentiment chart */}
      {Object.keys(sentiment).length > 0 && (
        <div className="mt-6 flex justify-center">
          <div className="w-full md:w-1/2 flex flex-col items-center">
            <h2 className="text-lg font-semibold mb-3 text-center">
              Sentiment Analysis
            </h2>
            <SentimentChart data={sentiment} />
          </div>
        </div>
      )}

      {/* Articles */}
      <div className="mt-6 space-y-6">
        {articles.map((article, i) => (
          <NewsCard key={i} article={article} />
        ))}
      </div>
    </div>
  )
}

export default App
