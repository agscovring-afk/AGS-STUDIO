import os

from app.ai.ui_generator.ui_templates import (
    class_name,
    PAGE_TEMPLATE,
    DIALOG_TEMPLATE
)


def generate_ui(module):

    cls = class_name(module)


    files = {

        f"app/ui/pages/{module}_page.py":
            PAGE_TEMPLATE.format(
                class_name=cls,
                module=module
            ),


        f"app/ui/dialogs/{module}_dialog.py":
            DIALOG_TEMPLATE.format(
                class_name=cls,
                module=module
            )
    }


    for path, content in files.items():

        with open(
            path,
            "w",
            encoding="utf-8"
        ) as f:

            f.write(content)


    print(
        f"[UI] Generated: {module}"
    )
