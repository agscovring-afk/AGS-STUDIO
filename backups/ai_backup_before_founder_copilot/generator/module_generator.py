import json
import os

from app.ai.generator.templates import (
    class_name,
    MODEL_TEMPLATE,
    REPOSITORY_TEMPLATE,
    SERVICE_TEMPLATE,
    CONTROLLER_TEMPLATE,
)

BASE = "app"
METADATA = "app/metadata/modules"


def load_metadata(module):

    path = os.path.join(
        METADATA,
        f"{module}.json"
    )

    if not os.path.exists(path):
        raise FileNotFoundError(path)

    with open(
        path,
        "r",
        encoding="utf-8"
    ) as f:
        return json.load(f)


def generate_module(module):

    metadata = load_metadata(module)

    cls = class_name(
        metadata["module"]
    )

    files = {

        f"models/{module}.py":
            MODEL_TEMPLATE.format(
                class_name=cls,
                module=module
            ),

        f"repositories/{module}_repository.py":
            REPOSITORY_TEMPLATE.format(
                class_name=cls,
                module=module
            ),

        f"services/{module}_service.py":
            SERVICE_TEMPLATE.format(
                class_name=cls,
                module=module
            ),

        f"controllers/{module}_controller.py":
            CONTROLLER_TEMPLATE.format(
                class_name=cls,
                module=module
            )

    }

    for path, content in files.items():

        full = os.path.join(
            BASE,
            path
        )

        os.makedirs(
            os.path.dirname(full),
            exist_ok=True
        )

        with open(
            full,
            "w",
            encoding="utf-8"
        ) as f:
            f.write(content)

    print(
        f"[GENERATOR] Generated from metadata: {module}"
    )