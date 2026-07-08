from ags.core.plugin_manager import PluginManager


class AGSEngine:

    def __init__(self):

        self.plugins = PluginManager()


    def start(self):

        self.plugins.discover()

        print(
            "AGS Engine started"
        )

        print(
            "Plugins:",
            self.plugins.list_plugins()
        )
