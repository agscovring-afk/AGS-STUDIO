from pathlib import Path


class ModuleGenerator:

    def generate(self, schema):

        module = schema["module"]

        base = Path(
            "app/modules/" + module
        )

        folders = [
            "models",
            "services",
            "api",
            "schemas",
            "tests"
        ]

        for folder in folders:
            (base / folder).mkdir(
                parents=True,
                exist_ok=True
            )

        for table in schema["tables"]:

            filename = table + ".py"

            class_name = (
                table.title()
                .replace("_", "")
            )

            content = (
                "class "
                + class_name
                + ":\n\n"
                + "    pass\n"
            )

            file = (
                base /
                "models" /
                filename
            )

            file.write_text(
                content,
                encoding="utf-8"
            )

        return str(base)


module_generator = ModuleGenerator()