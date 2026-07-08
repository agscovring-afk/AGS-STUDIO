from ags.core.plugin_manager import PluginManager

from app.ai.plugins.initializer import plugin_initializer


class AGSEngine:

    def __init__(self):

        self.plugins = PluginManager()
        self.ai_plugins = None


    def start(self):

        self.plugins.discover()

        self.ai_plugins = (
            plugin_initializer.initialize()
        )

        print(
            "AGS Engine started"
        )

        print(
            "Plugins:",
            self.plugins.list_plugins()
        )

        print(
            "AI Plugins:",
            self.ai_plugins
        )