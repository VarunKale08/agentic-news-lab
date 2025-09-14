import { PieChart, Pie, Cell, Legend, Tooltip } from "recharts"

const COLORS = {
  Positive: "#22c55e", // green
  Neutral: "#3b82f6",  // blue
  Negative: "#ef4444"  // red
}

function SentimentChart({ data }) {
  const chartData = Object.entries(data).map(([key, value]) => ({
    name: key,
    value
  }))

  return (
    <div className="bg-white rounded-lg shadow p-4 text-black">
      <h2 className="text-lg font-bold mb-4">Sentiment Distribution</h2>
      <PieChart width={300} height={300}>
        <Pie
          data={chartData}
          cx="50%"
          cy="50%"
          labelLine={false}
          outerRadius={100}
          dataKey="value"
        >
          {chartData.map((entry, index) => (
            <Cell
              key={`cell-${index}`}
              fill={COLORS[entry.name]}
            />
          ))}
        </Pie>
        <Tooltip />
        <Legend />
      </PieChart>
    </div>
  )
}

export default SentimentChart
