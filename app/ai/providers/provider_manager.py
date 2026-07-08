from app.ai.providers.ollama_provider import OllamaProvider


class ProviderManager:


    def __init__(self):

        self.providers = {

            "ollama": OllamaProvider(),

        }


    def register(self, name, provider):

        self.providers[name] = provider


    def get(self, name="ollama"):

        return self.providers.get(name)


    def available(self):

        return list(self.providers.keys())


    def run(self, prompt, provider=None):

        if provider:

            selected = self.get(provider)

            if selected:
                return selected.generate(prompt)


        for name, service in self.providers.items():

            try:

                return service.generate(prompt)

            except Exception:

                continue


        return {
            "status": "failed",
            "message": "No AI provider available"
        }