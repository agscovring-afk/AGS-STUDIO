from pathlib import Path
from ags.core.schema_manager import SchemaManager
from ags.core.template_manager import TemplateManager
from ags.registry import Registry


class ModuleGenerator:


    def __init__(self, root="."):

        self.root = Path(root)
        self.schema = SchemaManager()
        self.templates = TemplateManager()
        self.registry = Registry()


    def generate(self, name):

        schema = self.schema.load(name)

        if not schema:

            print(
                f"SCHEMA NOT FOUND: {name}"
            )

            return


        class_name = name.capitalize()

        data = {

            "class_name": class_name,

            "module": name,

            "fields": [
                type(
                    "Field",
                    (),
                    field
                )
                for field in schema.get("fields", [])
            ]

        }


        files = {

            f"app/models/{name}.py": "model.j2",
            f"app/repositories/{name}_repository.py": "repository.j2",
            f"app/services/{name}_service.py": "service.j2",
            f"app/controllers/{name}_controller.py": "controller.j2",
            f"app/ui/pages/{name}_page.py": "page.j2",
            f"app/ui/dialogs/{name}_dialog.py": "dialog.j2",

        }


        for file, template in files.items():

            path = self.root / file

            path.parent.mkdir(
                parents=True,
                exist_ok=True
            )

            path.write_text(
                self.templates.render(
                    template,
                    data
                ),
                encoding="utf-8"
            )

            print(
                "CREATED:",
                file
            )


        self.registry.register(name)
