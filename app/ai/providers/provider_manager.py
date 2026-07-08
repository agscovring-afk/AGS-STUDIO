from typing import Dict, Optional

from app.ai.plugins.plugin_manager import plugin_manager


class ProviderManager:
    """
    Unified AI Provider Manager.

    Connects existing AI providers with Plugin Runtime.
    """

    def __init__(self):
        self.plugins = plugin_manager

    # ==========================
    # Load provider plugins
    # ==========================

    def load(
        self,
        module: str,
        class_name: str
    ):

        return self.plugins.register(
            module,
            class_name
        )

    # ==========================
    # Get provider
    # ==========================

    def get(
        self,
        name: str
    ):

        return self.plugins.get(
            name
        )

    # ==========================
    # Chat
    # ==========================

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

    # ==========================
    # Status
    # ==========================

    def status(self) -> Dict:

        return self.plugins.status()


provider_manager = ProviderManager()