from typing import Dict, List, Optional
from app.ai.plugins.base.provider import AIProvider


class PluginRegistry:
    """
    Central registry for AI provider plugins.
    """

    def __init__(self):
        self._plugins: Dict[str, AIProvider] = {}

    # ==========================
    # Register
    # ==========================

    def register(
        self,
        plugin: AIProvider
    ):
        name = plugin.name

        if not name:
            raise ValueError(
                "Plugin must have a name"
            )

        self._plugins[name] = plugin

    # ==========================
    # Remove
    # ==========================

    def unregister(
        self,
        name: str
    ):
        self._plugins.pop(
            name,
            None
        )

    # ==========================
    # Get
    # ==========================

    def get(
        self,
        name: str
    ) -> Optional[AIProvider]:

        return self._plugins.get(name)

    # ==========================
    # Exists
    # ==========================

    def exists(
        self,
        name: str
    ) -> bool:

        return name in self._plugins

    # ==========================
    # List
    # ==========================

    def list_plugins(
        self
    ) -> List[str]:

        return list(
            self._plugins.keys()
        )

    # ==========================
    # Information
    # ==========================

    def describe(
        self
    ) -> Dict:

        return {
            name: plugin.info()
            for name, plugin in self._plugins.items()
        }


# Global registry instance

plugin_registry = PluginRegistry()