import json
from pathlib import Path

TASK_FILE = Path("storage/build_tasks.json")

class TaskManager:

    def create(self, name, description):
        TASK_FILE.parent.mkdir(exist_ok=True)

        data = {
            "project": name,
            "description": description,
            "status": "created",
            "steps": [
                "planning",
                "architecture",
                "development",
                "testing",
                "report"
            ]
        }

        TASK_FILE.write_text(
            json.dumps(data, indent=4),
            encoding="utf-8"
        )

        return data


task_manager = TaskManager()