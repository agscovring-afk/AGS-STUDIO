import requests

from app.ai.plugins.base.provider import AIProvider


class OllamaPlugin(AIProvider):
    """
    Ollama AI Provider Plugin.
    """

    name = "ollama"
    version = "1.0"
    capabilities = [
        "chat",
        "local",
        "reasoning"
    ]

    def __init__(self, config=None):

        super().__init__(config)

        self.url = self.config.get(
            "url",
            "http://localhost:11434/api/generate"
        )

        self.model_name = self.config.get(
            "model",
            "qwen2.5:3b"
        )

    # ==========================
    # Chat
    # ==========================

    def chat(
        self,
        prompt,
        context=None,
        **kwargs
    ):

        payload = {
            "model": self.model_name,
            "prompt": prompt,
            "stream": False
        }

        response = requests.post(
            self.url,
            json=payload,
            timeout=120
        )

        response.raise_for_status()

        data = response.json()

        return {
            "provider": self.name,
            "model": self.model_name,
            "response": data.get(
                "response",
                ""
            )
        }