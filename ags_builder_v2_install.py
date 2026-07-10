from pathlib import Path


BASE = Path("app/ai/autobuilder")


files = {

"schema_generator.py": '''
class SchemaGenerator:

    def generate(self, request):

        if "tender" in request.lower():

            return {
                "module": "tenders",
                "tables": [
                    "tenders",
                    "tender_documents",
                    "boq_items",
                    "supplier_quotes",
                    "tender_evaluations"
                ]
            }

        return {
            "module": "custom_module",
            "tables": []
        }


schema_generator = SchemaGenerator()
''',


"module_generator.py": '''
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

            content = (
                "class "
                + table.title().replace("_", "")
                + ":\n\n"
                + "    pass\n"
            )

            (base / "models" / filename).write_text(
                content,
                encoding="utf-8"
            )

        return str(base)


module_generator = ModuleGenerator()
''',


"code_agent.py": '''
from app.ai.autobuilder.schema_generator import schema_generator
from app.ai.autobuilder.module_generator import module_generator


class CodeAgent:

    def build(self, request):

        schema = schema_generator.generate(
            request
        )

        path = module_generator.generate(
            schema
        )

        return {
            "schema": schema,
            "generated": path
        }


code_agent = CodeAgent()
'''
}


for name, content in files.items():

    path = BASE / name

    path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    path.write_text(
        content.strip(),
        encoding="utf-8"
    )


print("AGS AUTONOMOUS BUILDER V2 installed")
print("Code Generator ready")