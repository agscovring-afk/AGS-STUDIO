import os
import json


PAGES_FILE = "app/registry/pages.json"
ROOT_REGISTRY = "registry.json"


def class_name(module):

    return ''.join(
        word.capitalize()
        for word in module.split('_')
    ) + "Page"



def scan_pages():

    pages = {}

    folder = "app/ui/pages"


    for file in os.listdir(folder):

        if file.endswith("_page.py"):

            module = file.replace(
                "_page.py",
                ""
            )


            pages[module] = (
                f"app.ui.pages.{module}_page.{class_name(module)}"
            )


    return pages



def update_root_registry(pages):

    modules = {}

    for module in pages:

        modules[module] = {
            "version": "1.0"
        }


    with open(
        ROOT_REGISTRY,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            {
                "modules": modules
            },
            f,
            indent=4
        )



def save_registry():

    pages = scan_pages()


    with open(
        PAGES_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            pages,
            f,
            indent=4
        )


    update_root_registry(pages)


    print("[REGISTRY] Pages updated")
    print("[REGISTRY] Root registry synchronized")