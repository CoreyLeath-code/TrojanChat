from __future__ import annotations

import os
from typing import Any

from ai.embeddings.cohere_embedder import CohereEmbedder


class PineconeSearch:
    """Pinecone alternative to the existing Qdrant semantic-search path."""

    def __init__(self, index_name: str | None = None):
        api_key = os.getenv("PINECONE_API_KEY", "").strip()
        self.index_name = (
            index_name or os.getenv("PINECONE_INDEX_NAME", "trojanchat")
        ).strip()
        self.namespace = os.getenv("PINECONE_NAMESPACE", "trojanchat").strip()

        if not api_key:
            raise RuntimeError(
                "PINECONE_API_KEY is required when VECTOR_SEARCH_BACKEND=pinecone."
            )
        if not self.index_name or not self.namespace:
            raise RuntimeError("PINECONE_INDEX_NAME and PINECONE_NAMESPACE are required.")

        from pinecone import Pinecone

        self.index = Pinecone(api_key=api_key).Index(self.index_name)
        self.embedder = CohereEmbedder()

    def search(
        self,
        query: str,
        top_k: int = 5,
        filter_condition: dict[str, Any] | None = None,
    ) -> list[dict[str, Any]]:
        vector = self.embedder.embed_text(query)
        response = self.index.query(
            vector=vector,
            top_k=top_k,
            include_metadata=True,
            namespace=self.namespace,
            filter=filter_condition,
        )
        return [
            {
                "id": match.id,
                "score": match.score,
                "payload": match.metadata or {},
            }
            for match in response.matches
        ]
