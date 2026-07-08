from app.ai.providers.ollama_provider import OllamaProvider



class ProviderManager:


    def __init__(self):

        self.providers = {

            "ollama": OllamaProvider()

        }



    def get(self, name="ollama"):

        return self.providers.get(
            name
        )