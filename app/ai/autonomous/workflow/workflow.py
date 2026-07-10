from datetime import datetime


class Workflow:


    def __init__(self, name):

        self.name = name
        self.steps = []
        self.status = "CREATED"
        self.created_at = datetime.now().isoformat()


    def add_step(self, step):

        self.steps.append(
            {
                "name": step,
                "status": "PENDING"
            }
        )


    def start(self):

        self.status = "RUNNING"


    def complete_step(self, name):

        for step in self.steps:

            if step["name"] == name:
                step["status"] = "COMPLETED"


    def progress(self):

        if not self.steps:
            return 0

        completed = len(
            [
                s for s in self.steps
                if s["status"] == "COMPLETED"
            ]
        )

        return int(
            (completed / len(self.steps)) * 100
        )


    def data(self):

        return {
            "name": self.name,
            "status": self.status,
            "progress": self.progress(),
            "steps": self.steps
        }