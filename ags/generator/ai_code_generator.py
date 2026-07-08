import os


class AICodeGenerator:


    def __init__(self):

        self.base = "app"


    def create_file(self, path, content):

        os.makedirs(
            os.path.dirname(path),
            exist_ok=True
        )

        with open(
            path,
            "w",
            encoding="utf-8"
        ) as f:

            f.write(content)

        print(
            "CREATED:",
            path
        )


    def generate(self, module, context):

        module_class = module.capitalize()


        files = {


            f"{self.base}/models/{module}.py":
f'''class {module_class}Model:


    def __init__(self):
        pass


    def save(self):
        pass
''',



            f"{self.base}/services/{module}_service.py":
f'''class {module_class}Service:


    def create(self, data):

        return data


    def update(self, data):

        return data
''',



            f"{self.base}/controllers/{module}_controller.py":
f'''from app.services.{module}_service import {module_class}Service


class {module_class}Controller:


    def __init__(self):

        self.service = {module_class}Service()
''',



            f"{self.base}/ui/pages/{module}_page.py":
f'''class {module_class}Page:


    def show(self):

        print("{module} page")
''',



            f"{self.base}/ui/dialogs/{module}_dialog.py":
f'''class {module_class}Dialog:


    def open(self):

        print("{module} dialog")
'''

        }


        for path, content in files.items():

            self.create_file(
                path,
                content
            )


        return self.base
