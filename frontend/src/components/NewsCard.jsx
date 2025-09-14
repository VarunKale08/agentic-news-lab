function NewsCard({ article }) {
  const { headline, summary, sentiment, source, url, publish_date } = article

  // Badge color mapping
  const sentimentColors = {
    Positive: "bg-green-100 text-green-700 border border-green-400",
    Negative: "bg-red-100 text-red-700 border border-red-400",
    Neutral: "bg-gray-200 text-gray-700 border border-gray-400",
  }

  return (
    <div className="bg-white text-black rounded-lg shadow p-4 mb-4 hover:shadow-lg transition">
      {/* Headline */}
      <h2 className="text-xl font-bold mb-2">
        <a
          href={url}
          target="_blank"
          rel="noopener noreferrer"
          className="hover:underline text-blue-600"
        >
          {headline}
        </a>
      </h2>

      {/* Summary */}
      <p className="text-gray-700 mb-3">{summary}</p>

      {/* Source + Date + Sentiment */}
      <div className="flex justify-between items-center text-sm text-gray-600 mb-3">
        <span>{source}</span>
        <span>{new Date(publish_date).toLocaleString()}</span>
      </div>

      {/* Sentiment Badge */}
      <div>
        <span
          className={`inline-block px-3 py-1 text-xs font-semibold rounded-full ${sentimentColors[sentiment] || "bg-gray-200 text-gray-700"}`}
        >
          {sentiment}
        </span>
      </div>
    </div>
  )
}

export default NewsCard
