from .base_worker import BaseWorker


class ModuleBuilderWorker(BaseWorker):

    name = "MODULE_BUILDER_WORKER"


    def execute(self, task):

        from .bridge import bridge


        module = task.get(
            "module",
            "sample"
        )


        files = [

            {
                "path": f"generated/{module}/model.py",
                "content":
                f"class {module.title()}Model:\n    pass\n"
            },

            {
                "path": f"generated/{module}/service.py",
                "content":
                f"class {module.title()}Service:\n    pass\n"
            },

            {
                "path": f"generated/{module}/controller.py",
                "content":
                f"class {module.title()}Controller:\n    pass\n"
            },

            {
                "path": f"generated/{module}/ui.py",
                "content":
                f"class {module.title()}UI:\n    pass\n"
            },

            {
                "path": f"generated/{module}/tests.py",
                "content":
                "def test_module():\n    assert True\n"
            }
        ]


        result = bridge.dispatch(
            "file_creator",
            {
                "files": files
            }
        )


        return self.report(
            task,
            result
        )
