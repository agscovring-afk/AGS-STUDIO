import json
from pathlib import Path


class Registry:


    def __init__(self, file="registry.json"):

        self.file = Path(file)

        if not self.file.exists():

            self.save(
                {
                    "modules": {}
                }
            )


    def load(self):

        return json.loads(
            self.file.read_text(
                encoding="utf-8"
            )
        )


    def save(self, data):

        self.file.write_text(
            json.dumps(
                data,
                indent=4
            ),
            encoding="utf-8"
        )


    def register(self, name):

        data = self.load()

        data["modules"][name] = {

            "version": "1.0"

        }

        self.save(data)


        print(
            "REGISTERED:",
            name
        )


    def list(self):

        return self.load()["modules"]
