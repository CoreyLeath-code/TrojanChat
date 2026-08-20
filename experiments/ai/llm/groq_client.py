import os
from typing import Optional, Dict, Any
from groq import Groq


class GroqClient:
    """
    Wrapper for interacting with the Groq LLM API.
    Handles prompt submission, response parsing, and error handling.
    """

    def __init__(self, api_key: Optional[str] = None, model: str = "llama3-70b-8192"):
        self.api_key = api_key or os.getenv("GROQ_API_KEY")

        if not self.api_key:
            raise ValueError("GROQ_API_KEY is not set in environment variables.")

        self.client = Groq(api_key=self.api_key)
        self.model = model

    def generate_response(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 512,
    ) -> Dict[str, Any]:
        """
        Sends a prompt to the Groq LLM and returns structured response.
        """

        try:
            messages = []

            # System prompt (controls behavior/personality)
            if system_prompt:
                messages.append({
                    "role": "system",
                    "content": system_prompt
                })

            # User input
            messages.append({
                "role": "user",
                "content": prompt
            })

            completion = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
            )

            response_text = completion.choices[0].message.content

            return {
                "success": True,
                "response": response_text,
                "model": self.model,
                "usage": {
                    "prompt_tokens": getattr(completion.usage, "prompt_tokens", None),
                    "completion_tokens": getattr(completion.usage, "completion_tokens", None),
                    "total_tokens": getattr(completion.usage, "total_tokens", None),
                }
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    def stream_response(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 512,
    ):
        """
        Streams response tokens from Groq (useful for real-time chat UI).
        """

        try:
            messages = []

            if system_prompt:
                messages.append({
                    "role": "system",
                    "content": system_prompt
                })

            messages.append({
                "role": "user",
                "content": prompt
            })

            stream = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                stream=True,
            )

            for chunk in stream:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content

        except Exception as e:
            yield f"[ERROR]: {str(e)}"