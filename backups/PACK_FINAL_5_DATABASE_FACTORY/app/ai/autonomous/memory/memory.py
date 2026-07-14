from datetime import datetime


class AutonomousMemory:

    def __init__(self):
        self.records = []


    def remember(self, key, value, category="GENERAL"):

        record = {
            "key": key,
            "value": value,
            "category": category,
            "time": datetime.now().isoformat()
        }

        self.records.append(record)

        return record


    def all(self):

        return self.records


    def clear(self):

        self.records = []


memory = AutonomousMemory()