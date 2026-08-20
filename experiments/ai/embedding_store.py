import numpy as np
from openai import OpenAI
import os

class EmbeddingStore:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.vectors = []
        self.texts = []

    def add(self, text: str):
        emb = self.client.embeddings.create(
            model="text-embedding-3-small",
            input=text
        ).data[0].embedding

        self.vectors.append(emb)
        self.texts.append(text)

    def search(self, query: str, k: int = 3):
        emb = self.client.embeddings.create(
            model="text-embedding-3-small",
            input=query
        ).data[0].embedding

        scores = [np.dot(emb, v) for v in self.vectors]
        top_idx = np.argsort(scores)[-k:]

        return [self.texts[i] for i in top_idx]