from .base_worker import BaseWorker
import re


class ModuleBuilderWorker(BaseWorker):

    name = "REAL_ERP_MODULE_BUILDER_V1"


    def normalize_module_name(self, request):

        text = request.lower()

        remove_words = [
            "create",
            "build",
            "generate",
            "erp",
            "module",
            "system",
            "real"
        ]

        for word in remove_words:
            text = text.replace(word, "")

        text = re.sub(
            r"[^a-z0-9_ ]",
            "",
            text
        )

        text = "_".join(
            text.split()
        )

        return text.strip("_") or "sample"


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
