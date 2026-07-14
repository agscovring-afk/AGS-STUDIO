from datetime import datetime

class AGSProjectManager:

    def __init__(self):
        self.system = "AGS AUTONOMOUS PROJECT MANAGER V1"
        self.projects = {}

    def create(self, name):

        project = {
            "name": name,
            "status": "CREATED",
            "progress": 0,
            "tasks": [],
            "logs": [],
            "created": str(datetime.now())
        }

        self.projects[name] = project

        return {
            "system": self.system,
            "project": name,
            "status": "CREATED",
            "tracking": "ACTIVE",
            "dashboard": "READY"
        }


project_manager = AGSProjectManager()
