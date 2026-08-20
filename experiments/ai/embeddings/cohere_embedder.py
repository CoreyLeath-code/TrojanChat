import os
import cohere


class CohereEmbedder:
    """
    Handles embedding generation using Cohere.
    """

    def __init__(self):
        api_key = os.getenv("COHERE_API_KEY")

        if not api_key:
            raise ValueError("COHERE_API_KEY not set.")

        self.client = cohere.Client(api_key)

    def embed_text(self, text: str):
        response = self.client.embed(
            texts=[text],
            model="embed-english-v3.0"
        )

        return response.embeddings[0]