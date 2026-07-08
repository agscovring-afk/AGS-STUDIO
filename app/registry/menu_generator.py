import json


REGISTRY_FILE = "app/registry/pages.json"


def generate_menu():

    with open(
        REGISTRY_FILE,
        "r",
        encoding="utf-8"
    ) as f:

        pages = json.load(f)


    menu = []

    for name in pages:

        menu.append(
            {
                "name": name.capitalize(),
                "route": name
            }
        )


    with open(
        "app/registry/menu.json",
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            menu,
            f,
            indent=4
        )


    print("[MENU] Generated")