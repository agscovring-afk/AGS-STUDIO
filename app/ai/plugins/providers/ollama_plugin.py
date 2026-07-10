import requests

from app.ai.plugins.base.provider import AIProvider


class OllamaPlugin(AIProvider):

    name = "ollama"
    version = "1.0"
    capabilities = ["chat", "generation"]


    def __init__(self):
        super().__init__()

        self.url = "http://localhost:11434/api/generate"
        self.model = "qwen2.5:3b"



    def chat(self, prompt, **kwargs):

        payload = {

            "model": self.model,

            "prompt": prompt,

            "stream": False,

            "options": {

                "temperature": 0.3,

                "num_ctx": 4096

            }

        }


        response = requests.post(

            self.url,

            json=payload,

            timeout=600

        )


        response.raise_for_status()


        data = response.json()


        return data.get(

            "response",

            ""

        )
