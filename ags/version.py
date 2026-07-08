import json
from pathlib import Path


class VersionManager:


    def __init__(self, file="registry.json"):

        self.file = Path(file)


    def get_version(self, name):

        data = json.loads(
            self.file.read_text(
                encoding="utf-8"
            )
        )

        return data["modules"][name]["version"]


    def upgrade(self, name):

        data = json.loads(
            self.file.read_text(
                encoding="utf-8"
            )
        )

        current = data["modules"][name]["version"]

        major, minor = current.split(".")

        minor = int(minor) + 1

        new_version = f"{major}.{minor}"


        data["modules"][name]["version"] = new_version


        self.file.write_text(
            json.dumps(
                data,
                indent=4
            ),
            encoding="utf-8"
        )


        return new_version
