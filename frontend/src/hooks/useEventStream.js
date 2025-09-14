import { useEffect } from "react"

export function useEventStream(url, onMessage) {
  useEffect(() => {
    const eventSource = new EventSource(url)

    eventSource.onmessage = (event) => {
      onMessage(event.data)
    }

    eventSource.onerror = (error) => {
      console.error("SSE error:", error)
      eventSource.close()
    }

    return () => {
      eventSource.close()
    }
  }, [url])
}
