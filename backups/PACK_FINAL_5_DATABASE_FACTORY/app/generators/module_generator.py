import json
from pathlib import Path

from app.generators.models.model_generator import ModelGenerator
from app.generators.database.database_generator import DatabaseGenerator
from app.generators.services.service_generator import ServiceGenerator
from app.generators.api.api_generator import APIGenerator
from app.generators.ui.qt_generator import QtGenerator
from app.generators.validators.module_validator import ModuleValidator


class ModuleGenerator:

    def __init__(self):

        self.model = ModelGenerator()
        self.database = DatabaseGenerator()
        self.service = ServiceGenerator()
        self.api = APIGenerator()
        self.ui = QtGenerator()
        self.validator = ModuleValidator()


    def create(self,module):

        module = module.lower()

        base = Path("generated") / module

        for folder in [

            "metadata",

            "models",

            "services",

            "api",

            "ui",

            "database",

            "tests",

            "docs"

        ]:

            (base / folder).mkdir(parents=True, exist_ok=True)

        (base / "metadata" / f"{module}.json").write_text(

            json.dumps(

                {

                    "name": module,

                    "version": "1.5.0",

                    "generated_by": "AGS-STUDIO"

                },

                indent=4

            ),

            encoding="utf8"

        )

        generated = []

        generated.append(self.model.generate(module))
        generated.append(self.database.generate(module))
        generated.append(self.service.generate(module))
        generated.append(self.api.generate(module))
        generated.append(self.ui.generate(module))

        validation = self.validator.validate(module)

        return {

            "status": "success",

            "module": module,

            "generated": generated,

            "validation": validation

        }
