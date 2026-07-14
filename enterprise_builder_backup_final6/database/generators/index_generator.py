from pathlib import Path
import json


class IndexGenerator:

    def __init__(self, workspace):
        self.workspace = Path(workspace)
        self.output = self.workspace / "database"

    def generate(self, metadata):

        self.output.mkdir(parents=True, exist_ok=True)

        file = self.output / "indexes.json"

        indexes = {
            "entities": [
                e.__dict__ if hasattr(e, "__dict__") else e
                for e in metadata.get("entities", [])
            ],
            "strategy": [
                "primary_keys",
                "foreign_keys",
                "tenant_indexes"
            ]
        }

        file.write_text(
            json.dumps(indexes, indent=4, ensure_ascii=False, default=str),
            encoding="utf-8"
        )

        return str(file)
