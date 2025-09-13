import requests


class OllamaEmbeddings:
    def __init__(self, model="mxbai-embed-large", base_url="http://localhost:11434"):
        self.model = model
        self.base_url = base_url

    def embed(self, texts):
        """Return list of embeddings for a string or list of strings"""
        if isinstance(texts, str):
            texts = [texts]

        embeddings = []
        for text in texts:
            resp = requests.post(
                f"{self.base_url}/api/embeddings",
                json={"model": self.model, "prompt": text},
                timeout=60,
            )
            resp.raise_for_status()
            data = resp.json()
            embeddings.append(data["embedding"])
        return embeddings
