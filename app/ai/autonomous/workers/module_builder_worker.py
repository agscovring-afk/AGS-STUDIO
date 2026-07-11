import re

from .base_worker import BaseWorker


class ModuleBuilderWorker(BaseWorker):

    name = "MODULE_BUILDER_WORKER"


    REMOVE_WORDS = [
        "build",
        "create",
        "generate",
        "module",
        "system",
        "with",
        "for",
        "the",
        "a",
        "an"
    ]


    MAX_MODULE_NAME_LENGTH = 50


    def normalize_module_name(self, text):

        text = text.lower()


        for word in self.REMOVE_WORDS:
            text = text.replace(
                word,
                ""
            )


        text = re.sub(
            r"[^a-z0-9_ ]",
            "",
            text
        )


        text = "_".join(
            text.split()
        )


        text = text.strip("_")


        if len(text) > self.MAX_MODULE_NAME_LENGTH:

            text = (
                text[:self.MAX_MODULE_NAME_LENGTH]
                .rstrip("_")
            )


        return text or "sample"



    def execute(self, task):

        from .bridge import bridge


        request = task.get(
            "request",
            ""
        )


        module = self.normalize_module_name(
            request
        )


        files = [

            {
                "path": f"generated/modules/{module}/models/{module}.py",
                "content":
f'''class {module.title().replace("_","")}Model:


    def __init__(self):
        self.table = "{module}"

'''
            },


            {
                "path": f"generated/modules/{module}/services/{module}_service.py",
                "content":
f'''class {module.title().replace("_","")}Service:


    def create(self, data):
        return data


    def update(self, data):
        return data


    def delete(self, item_id):
        return True

'''
            },


            {
                "path": f"generated/modules/{module}/controllers/{module}_controller.py",
                "content":
f'''class {module.title().replace("_","")}Controller:


    def index(self):

        return {{
            "module": "{module}",
            "status": "ready"
        }}

'''
            },


            {
                "path": f"generated/modules/{module}/ui/{module}_page.py",
                "content":
f'''class {module.title().replace("_","")}Page:


    def render(self):

        return "{module} UI READY"

'''
            },


            {
                "path": f"generated/modules/{module}/tests/test_{module}.py",
                "content":
'''def test_module():

    assert True

'''
            },


            {
                "path": f"generated/modules/{module}/metadata.json",
                "content":
f'''{{
    "module": "{module}",
    "type": "ERP",
    "status": "generated",
    "version": "V1"
}}
'''
            }

        ]


        result = bridge.dispatch(
            "file_creator",
            {
                "files": files
            }
        )


        return self.report(
            {
                "module": module,
                "request": request
            },
            result
        )
