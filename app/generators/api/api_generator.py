from pathlib import Path


class APIGenerator:

    def generate(self,module):

        module = module.lower()

        cls = module.capitalize()

        path = Path("generated") / module / "api"

        path.mkdir(parents=True, exist_ok=True)

        code = f'''from generated.{module}.services.{module}_service import {cls}Service

service = {cls}Service()


def create(data):

    return service.create(data)


def get(id):

    return service.get(id)


def list_all():

    return service.list()


def update(id,data):

    return service.update(id,data)


def delete(id):

    return service.delete(id)
'''

        file = path / f"{module}_api.py"

        file.write_text(code, encoding="utf8")

        return {

            "generator":"APIGenerator",

            "status":"success",

            "file":str(file)

        }

