import importlib
from typing import List, Type

from app.ai.plugins.base.provider import AIProvider
from app.ai.plugins.registry.plugin_registry import plugin_registry


class PluginLoader:
    """
    Dynamic AI Plugin Loader.

    Responsible for importing provider plugins
    and registering them into the runtime registry.
    """

    def __init__(self):
        self.loaded = []

    # ==========================
    # Load single plugin
    # ==========================

    def load(
        self,
        module_path: str,
        class_name: str
    ) -> AIProvider:

        module = importlib.import_module(
            module_path
        )

        plugin_class: Type[AIProvider] = getattr(
            module,
            class_name
        )

        plugin = plugin_class()

        if not isinstance(plugin, AIProvider):
            raise TypeError(
                "Plugin must inherit AIProvider"
            )

        plugin_registry.register(
            plugin
        )

        self.loaded.append(
            plugin.name
        )

        return plugin

    # ==========================
    # Load multiple plugins
    # ==========================

    def load_many(
        self,
        plugins: List[dict]
    ):

        result = []

        for item in plugins:

            plugin = self.load(
                item["module"],
                item["class"]
            )

            result.append(
                plugin.name
            )

        return result

    # ==========================
    # Status
    # ==========================

    def status(self):

        return {
            "loaded": self.loaded,
            "count": len(self.loaded)
        }


plugin_loader = PluginLoader()