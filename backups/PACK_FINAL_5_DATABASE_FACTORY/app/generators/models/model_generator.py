from pathlib import Path


class ModelGenerator:

    def generate(self, module):

        module = module.lower()

        model_name = module.capitalize()

        path = Path("generated") / module / "models"

        path.mkdir(parents=True, exist_ok=True)

        code = f'''from dataclasses import dataclass
from datetime import datetime


@dataclass
class {model_name}:

    id: int | None = None

    code: str = ""

    name: str = ""

    description: str = ""

    active: bool = True

    created_at: datetime | None = None

    updated_at: datetime | None = None
'''

        file = path / f"{module}.py"

        file.write_text(
            code,
            encoding="utf8"
        )

        return {
            "generator": "ModelGenerator",
            "status": "success",
            "file": str(file)
        }
