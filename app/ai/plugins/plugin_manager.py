from typing import Dict, Optional

from app.ai.plugins.loader.plugin_loader import plugin_loader
from app.ai.plugins.registry.plugin_registry import plugin_registry


class PluginManager:
    """
    High level manager for AI plugins.

    Handles loading, accessing and monitoring providers.
    """

    def __init__(self):
        self.loader = plugin_loader
        self.registry = plugin_registry

    # ==========================
    # Register plugin manually
    # ==========================

    def register(
        self,
        module: str,
        class_name: str
    ):

        return self.loader.load(
            module,
            class_name
        )

    # ==========================
    # Load from configuration
    # ==========================

    def load_plugins(
        self,
        plugins: list
    ):

        return self.loader.load_many(
            plugins
        )

    # ==========================
    # Get provider
    # ==========================

    def get(
        self,
        name: str
    ):

        return self.registry.get(
            name
        )

    # ==========================
    # Available providers
    # ==========================

    def available(self):

        return self.registry.list_plugins()

    # ==========================
    # Status
    # ==========================

    def status(self) -> Dict:

        return {
            "plugins": self.registry.describe(),
            "loader": self.loader.status()
        }


plugin_manager = PluginManager()