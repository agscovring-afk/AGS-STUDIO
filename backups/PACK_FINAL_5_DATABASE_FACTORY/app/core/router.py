import importlib
import json


REGISTRY_FILE = "app/registry/pages.json"


class Router:

    routes = {}


    @classmethod
    def load_registry(cls):

        with open(
            REGISTRY_FILE,
            "r",
            encoding="utf-8"
        ) as f:

            cls.routes = json.load(f)



    @classmethod
    def load(cls, name, parent):

        if name not in cls.routes:

            return None


        module_path, class_name = cls.routes[name].rsplit(".",1)


        module = importlib.import_module(
            module_path
        )


        page_class = getattr(
            module,
            class_name
        )


        try:

            return page_class(parent)

        except TypeError:

            return page_class()