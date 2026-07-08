import requests
from ags.ai.settings import AI_MODEL, AI_TIMEOUT


class OllamaProvider:

    name = "ollama"

    def __init__(self):

        self.model = AI_MODEL
        self.timeout = AI_TIMEOUT
        self.url = "http://127.0.0.1:11434"

    def available(self):

        try:

            response = requests.get(
                f"{self.url}/api/tags",
                timeout=3
            )

            return response.status_code == 200

        except Exception:

            return False

    def execute(self, task):

        payload = {
            "model": self.model,
            "prompt": task,
            "stream": False
        }

        response = requests.post(
            f"{self.url}/api/generate",
            json=payload,
            timeout=self.timeout
        )

        response.raise_for_status()

        data = response.json()

        return {
            "provider": self.name,
            "model": self.model,
            "response": data.get("response", "")
        }
