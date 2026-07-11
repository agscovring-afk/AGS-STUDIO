class BaseModule:

    name = "BASE"

    def __init__(self):
        self.records = []

    def create(self, data):
        self.records.append(data)
        return data

    def list(self):
        return self.records
