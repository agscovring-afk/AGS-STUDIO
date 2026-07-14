import os

from app.ai.crud_generator.crud_templates import (
    class_name,
    PAGE_TEMPLATE,
    DIALOG_TEMPLATE
)


def generate_crud(module):

    cls = class_name(module)


    page = PAGE_TEMPLATE.format(
        class_name=cls,
        module=module
    )


    dialog = DIALOG_TEMPLATE.format(
        class_name=cls,
        module=module
    )


    with open(
        f"app/ui/pages/{module}_page.py",
        "w",
        encoding="utf-8"
    ) as f:

        f.write(page)


    with open(
        f"app/ui/dialogs/{module}_dialog.py",
        "w",
        encoding="utf-8"
    ) as f:

        f.write(dialog)


    print(
        f"[CRUD] Generated: {module}"
    )
