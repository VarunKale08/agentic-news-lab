import axios from "axios";

const API_URL = import.meta.env.VITE_API_URL ?? "http://127.0.0.1:8000";

export async function fetchNews(topic) {
  const res = await axios.get(`${API_URL}/api/news`, {
    params: { topic },
    timeout: 600000, // 60s while the crew works
  });
  return res.data; // { topic, articles, sentiment_distribution }
}
