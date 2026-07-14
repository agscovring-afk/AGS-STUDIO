from typing import Dict

from app.ai.plugins.loader.plugin_loader import plugin_loader
from app.ai.plugins.registry.plugin_registry import plugin_registry


class PluginManager:

    def __init__(self):
        self.loader = plugin_loader
        self.registry = plugin_registry


    def register(self, *args):

        # old style:
        # register(module, class_name)

        if len(args) == 2:

            module = args[0]
            class_name = args[1]

            plugin = self.loader.load(
                module,
                class_name
            )

            self.registry.register(
                plugin
            )

            return plugin


        # new style:
        # register(name,module,class)

        if len(args) == 3:

            name = args[0]
            module = args[1]
            class_name = args[2]

            plugin = self.loader.load(
                module,
                class_name
            )

            self.registry.register(
                plugin
            )

            return plugin


        raise Exception(
            "Invalid plugin register format"
        )


    def load_plugins(self, plugins:list):

        result=[]

        for item in plugins:

            result.append(
                self.register(
                    item["module"],
                    item["class"]
                )
            )

        return result


    def get(self,name:str):

        return self.registry.get(
            name
        )


    def available(self):

        return self.registry.list_plugins()


    def status(self)->Dict:

        return {
            "plugins": self.registry.describe(),
            "loader": self.loader.status()
        }


plugin_manager = PluginManager()
