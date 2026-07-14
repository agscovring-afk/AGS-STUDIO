from pathlib import Path
import json


class EnterpriseRegistry:

    def __init__(self):
        self.file = Path("enterprise_registry.json")


    def register(self, name, data):
        registry = {}

        if self.file.exists():
            registry = json.loads(
                self.file.read_text()
            )

        registry[name] = data

        self.file.write_text(
            json.dumps(
                registry,
                indent=4
            )
        )


    def list(self):
        if not self.file.exists():
            return {}

        return json.loads(
            self.file.read_text()
        )
