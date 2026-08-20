import os
from typing import List, Dict, Any
from qdrant_client import QdrantClient
from qdrant_client.models import Filter
from ai.embeddings.cohere_embedder import CohereEmbedder


class QdrantSearch:
    """
    Handles vector search using Qdrant.
    """

    def __init__(self, collection_name: str = "trojanchat"):
        self.host = os.getenv("QDRANT_HOST", "localhost")
        self.port = int(os.getenv("QDRANT_PORT", 6333))
        self.collection_name = collection_name

        self.client = QdrantClient(host=self.host, port=self.port)
        self.embedder = CohereEmbedder()

    def search(
        self,
        query: str,
        top_k: int = 5,
        filter_condition: Filter = None
    ) -> List[Dict[str, Any]]:
        """
        Perform semantic search on Qdrant.
        """

        try:
            query_vector = self.embedder.embed_text(query)

            results = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_vector,
                limit=top_k,
                query_filter=filter_condition
            )

            return [
                {
                    "id": res.id,
                    "score": res.score,
                    "payload": res.payload
                }
                for res in results
            ]

        except Exception as e:
            return [{"error": str(e)}]