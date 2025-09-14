import { useState } from "react"

function SearchBar({ onSearch }) {
  const [topic, setTopic] = useState("")

  const handleSubmit = (e) => {
    e.preventDefault()
    if (topic.trim()) {
      onSearch(topic)
    }
  }

  return (
    <form
      onSubmit={handleSubmit}
      className="flex w-full max-w-2xl mx-auto mt-10"
    >
      <input
        type="text"
        value={topic}
        onChange={(e) => setTopic(e.target.value)}
        placeholder="Enter a topic (e.g., Elon Musk)"
        className="flex-1 px-4 py-3 rounded-l-full 
                   bg-white text-black placeholder-gray-500
                   border border-gray-300 focus:ring-2 focus:ring-blue-500 focus:outline-none"
      />
      <button
        type="submit"
        className="px-6 py-3 bg-blue-500 hover:bg-blue-600 text-white 
                   font-semibold rounded-r-full border border-blue-500"
      >
        Search
      </button>
    </form>
  )
}

export default SearchBar
