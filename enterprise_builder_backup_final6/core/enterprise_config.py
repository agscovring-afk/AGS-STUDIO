import json
from pathlib import Path


class EnterpriseConfig:

    def __init__(self):
        self.file = Path("enterprise_config.json")


    def load(self):

        if not self.file.exists():

            data = {
                "name": "AGS_ENTERPRISE",
                "modules": [],
                "multi_tenant": True,
                "version": "1.0"
            }

            self.file.write_text(
                json.dumps(data, indent=4)
            )

        return json.loads(
            self.file.read_text()
        )


    def save(self, data):

        self.file.write_text(
            json.dumps(data, indent=4)
        )