from pathlib import Path
import json
from datetime import datetime


class MigrationGenerator:

    def __init__(self, workspace):
        self.workspace = Path(workspace)
        self.output = self.workspace / "database" / "migrations"

    def serialize(self, obj):
        if hasattr(obj, "__dict__"):
            return obj.__dict__
        if isinstance(obj, list):
            return [self.serialize(x) for x in obj]
        if isinstance(obj, dict):
            return {k:self.serialize(v) for k,v in obj.items()}
        return obj

    def generate(self, metadata):

        self.output.mkdir(parents=True, exist_ok=True)

        file = self.output / (
            f"migration_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        )

        data = self.serialize(metadata)

        file.write_text(
            json.dumps(data, indent=4, ensure_ascii=False, default=str),
            encoding="utf-8"
        )

        return str(file)
