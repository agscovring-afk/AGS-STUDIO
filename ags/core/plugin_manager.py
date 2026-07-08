from pathlib import Path
import importlib


class PluginManager:

    def __init__(self, plugin_path="ags/plugins"):
        self.plugin_path = Path(plugin_path)
        self.plugins = {}

    def discover(self):

        if not self.plugin_path.exists():
            return

        for file in self.plugin_path.glob("*.py"):

            if file.name.startswith("_"):
                continue

            name = file.stem

            module = importlib.import_module(
                f"ags.plugins.{name}"
            )

            self.plugins[name] = module

        return self.plugins


    def load(self, name):

        if name in self.plugins:
            return self.plugins[name]

        return None


    def list_plugins(self):

        return list(self.plugins.keys())
