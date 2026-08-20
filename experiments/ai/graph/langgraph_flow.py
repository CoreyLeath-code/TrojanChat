from ai.llm.groq_client import GroqClient
from ai.retrieval.qdrant_search import QdrantSearch


class TrojanChatAI:
    """
    Core AI orchestration (RAG pipeline)
    """

    def __init__(self):
        self.llm = GroqClient()
        self.retriever = QdrantSearch()

    def run(self, user_query: str):
        # Step 1: Retrieve relevant context
        docs = self.retriever.search(user_query)

        context = "\n".join([
            d.get("payload", {}).get("text", "")
            for d in docs if "payload" in d
        ])

        # Step 2: Build prompt
        prompt = f"""
        You are a USC football expert.

        Context:
        {context}

        Question:
        {user_query}
        """

        # Step 3: Generate response
        result = self.llm.generate_response(prompt)

        return result