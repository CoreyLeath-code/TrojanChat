from openai import OpenAI
import os

class Moderator:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def check(self, message: str) -> bool:
        """
        Returns True if message is SAFE.
        Returns False if message violates guidelines.
        """
        result = self.client.moderations.create(
            model="omni-moderation-latest",
            input=message
        )

        flagged = result.results[0].flagged
        return not flagged