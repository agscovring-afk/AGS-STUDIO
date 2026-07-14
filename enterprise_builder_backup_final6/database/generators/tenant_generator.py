from pathlib import Path
import json


class TenantGenerator:

    def __init__(self, workspace):
        self.workspace = Path(workspace)
        self.output = self.workspace / "database"

    def generate(self, metadata):

        self.output.mkdir(parents=True, exist_ok=True)

        file = self.output / "tenant_rules.json"

        rules = {
            "multi_tenant": True,
            "strategy": "tenant_id_isolation",
            "entities": [
                e.__dict__ if hasattr(e, "__dict__") else e
                for e in metadata.get("entities", [])
            ]
        }

        file.write_text(
            json.dumps(
                rules,
                indent=4,
                ensure_ascii=False,
                default=str
            ),
            encoding="utf-8"
        )

        return str(file)
