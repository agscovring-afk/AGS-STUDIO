from app.ai.providers.provider_manager import ProviderManager


class AIRouter:


    def __init__(self):

        self.manager = ProviderManager()



    def ask(self, prompt, task="general"):


        if task == "code":

            provider = "ollama"

        elif task == "architecture":

            provider = "ollama"

        else:

            provider = "ollama"



        ai = self.manager.get(provider)


        if not ai:

            return {
                "status": "error",
                "message": "No provider available"
            }


        return ai.generate(prompt)