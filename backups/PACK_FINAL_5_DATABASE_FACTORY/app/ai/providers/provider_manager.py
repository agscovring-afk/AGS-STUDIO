from typing import Dict

from app.ai.plugins.plugin_manager import plugin_manager


class ProviderManager:
    """
    Unified AI Provider Manager.
    Loads default AI providers automatically.
    """

    def __init__(self):

        self.plugins = plugin_manager

        self.load_defaults()


    def load_defaults(self):

        try:

            self.plugins.register(
                "app.ai.plugins.providers.ollama_plugin",
                "OllamaPlugin"
            )

            print("[AI] Ollama provider loaded")

        except Exception as e:

            print(
                "[AI] Ollama loading failed:",
                e
            )


    def load(
        self,
        module: str,
        class_name: str
    ):

        return self.plugins.register(
            module,
            class_name
        )


    def get(
        self,
        name: str
    ):

        return self.plugins.get(
            name
        )


    def chat(
        self,
        provider: str,
        prompt: str,
        **kwargs
    ):

        instance = self.get(
            provider
        )

        if not instance:

            raise Exception(
                f"Provider not found: {provider}"
            )


        return instance.chat(
            prompt,
            **kwargs
        )


    def status(self) -> Dict:

        return self.plugins.status()



provider_manager = ProviderManager()