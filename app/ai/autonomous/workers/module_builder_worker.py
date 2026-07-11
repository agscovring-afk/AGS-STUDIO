class ModuleBuilderWorker:


    def normalize_module_name(self, text):

        import re


        remove_words = [
            "with",
            "and",
            "the",
            "for",
            "system",
            "module",
            "build",
            "create",
            "management",
            "erp",
        ]


        text = text.lower()


        for word in remove_words:
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


        return text[:60].strip("_") or "sample"



    def execute(self, task):


        if isinstance(task, dict):

            request = task.get(
                "request",
                ""
            )

        else:

            request = getattr(
                task,
                "description",
                ""
            )


        module = self.normalize_module_name(
            request
        )


        return {

            "status": "completed",

            "agent": "MODULE_BUILDER_AGENT",

            "module": module,

            "message": "Module build plan generated",

            "files": [

                f"generated/modules/{module}/models/{module}.py",

                f"generated/modules/{module}/services/{module}_service.py",

                f"generated/modules/{module}/controllers/{module}_controller.py",

                f"generated/modules/{module}/ui/{module}_page.py",

                f"generated/modules/{module}/tests/test_{module}.py"

            ]

        }
