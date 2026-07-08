from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional


class AIProvider(ABC):
    """
    Base interface for all AI providers.

    Every provider plugin must implement this contract:
    Ollama, OpenAI, Gemini, Claude, etc.
    """

    name: str = "unknown"
    version: str = "1.0"
    capabilities: List[str] = []

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.enabled = True

    # ==========================
    # Provider Information
    # ==========================

    def info(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "version": self.version,
            "capabilities": self.capabilities,
            "enabled": self.enabled,
        }

    # ==========================
    # Health
    # ==========================

    def health_check(self) -> Dict[str, Any]:
        return {
            "provider": self.name,
            "status": "ready" if self.enabled else "disabled",
        }

    # ==========================
    # Configuration
    # ==========================

    def configure(self, config: Dict[str, Any]):
        self.config.update(config)

    # ==========================
    # Chat
    # ==========================

    @abstractmethod
    def chat(
        self,
        prompt: str,
        context: Optional[List[Dict[str, str]]] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Execute AI completion.
        """
        pass

    # ==========================
    # Streaming
    # ==========================

    def stream(
        self,
        prompt: str,
        context: Optional[List[Dict[str, str]]] = None,
        **kwargs
    ):
        response = self.chat(
            prompt,
            context=context,
            **kwargs
        )

        yield response

    # ==========================
    # Embedding
    # ==========================

    def embedding(
        self,
        text: str
    ) -> List[float]:

        raise NotImplementedError(
            f"{self.name} does not support embeddings"
        )

    # ==========================
    # Model
    # ==========================

    def model(self) -> str:
        return self.config.get(
            "model",
            "default"
        )

    # ==========================
    # Shutdown
    # ==========================

    def shutdown(self):
        self.enabled = False