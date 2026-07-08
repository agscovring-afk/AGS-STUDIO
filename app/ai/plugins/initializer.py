from app.ai.plugins.discovery import plugin_discovery


class PluginInitializer:
    """
    Initializes AI Plugin Runtime at application startup.
    """

    def __init__(self):
        self.loaded = []

    def initialize(self):

        self.loaded = plugin_discovery.discover()

        return {
            "status": "initialized",
            "plugins": self.loaded
        }


plugin_initializer = PluginInitializer()