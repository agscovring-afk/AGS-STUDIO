import requests

from app.ai.providers.base_provider import BaseProvider



class OllamaProvider(BaseProvider):


    def __init__(self):

        self.url = "http://localhost:11434/api/generate"

        self.model = "qwen2.5:3b"



    def generate(self, prompt):

        data = {

            "model": self.model,

            "prompt": prompt,

            "stream": False

        }


        response = requests.post(
            self.url,
            json=data
        )


        result = response.json()


        return result.get(
            "response",
            ""
        )