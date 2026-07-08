from typing import Dict, Optional

from app.ai.providers.provider_manager import provider_manager
from app.ai.memory.memory_manager import memory_manager
from app.ai.memory.memory_types import MemoryType


class AIRouter:
    """
    AI routing layer with memory context.
    """

    def __init__(self):

        self.providers = provider_manager

        self.default_provider = None

        self.memory = memory_manager


    # ==========================
    # Provider
    # ==========================

    def set_default(
        self,
        provider: str
    ):

        self.default_provider = provider


    # ==========================
    # Build Context
    # ==========================

    def build_context(
        self,
        keyword=None
    ):

        context = []

        memories = self.memory.get_by_type(
            MemoryType.PROJECT
        )

        if keyword:

            memories += self.memory.search(
                keyword
            )


        for item in memories[-10:]:

            context.append({

                "role": "system",

                "content":
                    str(
                        item.get(
                            "content",
                            ""
                        )
                    )

            })

        return context


    # ==========================
    # Route
    # ==========================

    def route(
        self,
        prompt: str,
        provider: Optional[str] = None,
        memory_key=None,
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


        context = self.build_context(
            memory_key
        )


        return self.providers.chat(
            target,
            prompt,
            context=context,
            **kwargs
        )


    # ==========================
    # Health
    # ==========================

    def health(self) -> Dict:

        return {

            "router": "ready",

            "memory":
                "enabled",

            "providers":
                self.providers.status()

        }


ai_router = AIRouter()