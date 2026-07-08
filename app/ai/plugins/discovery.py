import os
import importlib
from typing import List

from app.ai.plugins.base.provider import AIProvider
from app.ai.plugins.registry.plugin_registry import plugin_registry


class PluginDiscovery:
    """
    Automatic discovery system for AI plugins.
    """

    def __init__(self):
        self.package = (
            "app.ai.plugins.providers"
        )

    # ==========================
    # Discover providers
    # ==========================

    def discover(self) -> List[str]:

        loaded = []

        path = self.package.replace(
            ".",
            os.sep
        )

        if not os.path.exists(path):
            return loaded

        for file in os.listdir(path):

            if not file.endswith(
                "_plugin.py"
            ):
                continue

            module_name = file[:-3]

            module = importlib.import_module(
                f"{self.package}.{module_name}"
            )

            for item in dir(module):

                obj = getattr(
                    module,
                    item
                )

                if (
                    isinstance(obj, type)
                    and issubclass(
                        obj,
                        AIProvider
                    )
                    and obj != AIProvider
                ):

                    plugin = obj()

                    plugin_registry.register(
                        plugin
                    )

                    loaded.append(
                        plugin.name
                    )

        return loaded


plugin_discovery = PluginDiscovery()