from pathlib import Path
import json
from dataclasses import asdict, is_dataclass


class SchemaGenerator:

    def __init__(self, workspace):
        self.workspace = Path(workspace)
        self.output = self.workspace / "database"


    def serialize(self, obj):

        if is_dataclass(obj):
            return asdict(obj)

        if hasattr(obj, "__dict__"):
            return {
                k: self.serialize(v)
                for k, v in obj.__dict__.items()
            }

        if isinstance(obj, list):
            return [
                self.serialize(x)
                for x in obj
            ]

        if isinstance(obj, dict):
            return {
                k: self.serialize(v)
                for k, v in obj.items()
            }

        return obj


    def generate(self, metadata):

        self.output.mkdir(
            parents=True,
            exist_ok=True
        )

        schema_file = self.output / "schema.json"

        schema = self.serialize(metadata)

        schema_file.write_text(
            json.dumps(
                schema,
                indent=4,
                ensure_ascii=False,
                default=str
            ),
            encoding="utf-8"
        )

        return str(schema_file)
