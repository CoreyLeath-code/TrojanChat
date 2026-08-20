import os
from openai import OpenAI
from typing import Dict

class LLMAgent:
    def __init__(self, model="gpt-4.1"):
        self.model = model
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def respond(self, message: str, username: str = "User") -> str:
        prompt = f"""
        You are TrojanChat AI Agent. You are inside a group chat.
        User: {username}
        Message: {message}

        Respond concisely, conversationally, and avoid long paragraphs.
        """

        chat = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}]
        )

        return chat.choices[0].message["content"]