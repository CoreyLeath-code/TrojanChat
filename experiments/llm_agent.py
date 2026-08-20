class LLMAgent:
    def __init__(self, model="gpt-4.1"):
        self.model = model
try:
    from llama_cpp import Llama

    class LocalLlamaAgent:
        def __init__(self, model_path="models/llama-3-8b.gguf"):
            self.llama = Llama(model_path=model_path)

        def respond(self, message: str) -> str:
            output = self.llama(
                f"User said: {message}. Respond as TrojanChat AI agent:",
                max_tokens=120
            )
            return output["choices"][0]["text"].strip()

except ImportError:
    LocalLlamaAgent = None
    def respond(self, prompt: str) -> str:
        return f"[AI-{self.model}] Placeholder response to: {prompt}"