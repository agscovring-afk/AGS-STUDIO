import json
import os


class ProjectMemory:


    def __init__(self):

        self.file = "data/project_memory.json"


    def save(self, data):

        os.makedirs("data", exist_ok=True)

        with open(
            self.file,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(data, f, indent=4)


        return {
            "status":"SAVED",
            "type":"PROJECT_MEMORY"
        }


    def load(self):

        if os.path.exists(self.file):

            with open(
                self.file,
                encoding="utf-8"
            ) as f:

                return json.load(f)

        return {}


memory = ProjectMemory()
