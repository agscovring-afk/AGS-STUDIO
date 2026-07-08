import json
from pathlib import Path


class SchemaManager:


    def __init__(self, path="schemas"):

        self.path = Path(path)


    def load(self, name):

        file = self.path / f"{name}.json"

        if not file.exists():

            return None


        return json.loads(
            file.read_text(
                encoding="utf-8-sig"
            )
        )


    def save(self, name, data):

        self.path.mkdir(
            parents=True,
            exist_ok=True
        )

        file = self.path / f"{name}.json"

        file.write_text(
            json.dumps(
                data,
                indent=4
            ),
            encoding="utf-8"
        )
