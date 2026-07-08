from typing import Dict, Optional

from app.ai.providers.provider_manager import provider_manager


class AIRouter:
    """
    Dynamic AI routing layer.

    Selects and executes AI providers through Plugin Runtime.
    """

    def __init__(self):
        self.providers = provider_manager
        self.default_provider = None

    # ==========================
    # Configure default
    # ==========================

    def set_default(
        self,
        provider: str
    ):
        self.default_provider = provider

    # ==========================
    # Available providers
    # ==========================

    def providers_list(self):

        return self.providers.status()

    # ==========================
    # Route request
    # ==========================

    def route(
        self,
        prompt: str,
        provider: Optional[str] = None,
        **kwargs
    ):

        target = (
            provider
            or self.default_provider
        )

        if not target:
            raise Exception(
                "No AI provider selected"
            )

        return self.providers.chat(
            target,
            prompt,
            **kwargs
        )

    # ==========================
    # Health
    # ==========================

    def health(self) -> Dict:

        return {
            "router": "ready",
            "providers": self.providers.status()
        }


ai_router = AIRouter()