from ags.ai.ollama_provider import OllamaProvider


class AIProvider:


    def __init__(self, name):

        self.name = name


    def available(self):

        return True


    def execute(self, task):

        return {

            "provider": self.name,

            "task": task,

            "status": "completed"

        }



class ProviderManager:


    def __init__(self):

        self.providers = [

            OllamaProvider(),

            AIProvider("local"),

            AIProvider("cloud_backup")

        ]


    def get_available(self):

        return [

            p for p in self.providers

            if p.available()

        ]
