import json


class UIMemoryEngine:

    def __init__(self, path="ui_memory.json"):
        self.path = path
        self.memory = {}


    def remember(self, key, value):

        self.memory[key] = value
        self.save()


    def recall(self, key):

        return self.memory.get(key)


    def save(self):

        with open(self.path,"w") as f:
            json.dump(
                self.memory,
                f,
                indent=4
            )
