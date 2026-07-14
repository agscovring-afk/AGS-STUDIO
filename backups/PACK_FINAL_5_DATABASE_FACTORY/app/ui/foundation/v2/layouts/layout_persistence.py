import json
import os


class LayoutPersistence:

    def __init__(self, path="layout.json"):

        self.path = path

    def save(self, data):

        with open(self.path, "w") as f:
            json.dump(data, f, indent=4)

    def load(self):

        if not os.path.exists(self.path):
            return {}

        with open(self.path) as f:
            return json.load(f)
