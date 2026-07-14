from pathlib import Path


class ServiceGenerator:

    def generate(self,module):

        module = module.lower()

        cls = module.capitalize()

        path = Path("generated") / module / "services"

        path.mkdir(parents=True, exist_ok=True)

        code = f'''from generated.{module}.models.{module} import {cls}


class {cls}Service:


    def create(self,data):

        return {cls}(**data)


    def get(self,id):

        pass


    def list(self):

        return []


    def update(self,id,data):

        pass


    def delete(self,id):

        pass
'''

        file = path / f"{module}_service.py"

        file.write_text(code,encoding="utf8")

        return {

            "generator":"ServiceGenerator",

            "status":"success",

            "file":str(file)

        }
