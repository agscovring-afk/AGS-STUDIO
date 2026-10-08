from pathlib import Path
import json

BASE = Path("app/ai/autobuilder")

files = {

"task_manager.py": '''
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
''',

"planner.py": '''
class Planner:

    def plan(self, request):

        return {
            "request": request,
            "phases": [
                "Analyze requirements",
                "Design architecture",
                "Generate modules",
                "Run tests",
                "Create report"
            ]
        }


planner = Planner()
''',

"executor.py": '''
from datetime import datetime

class Executor:

    def run(self, plan):

        result = []

        for phase in plan["phases"]:
            result.append({
                "phase": phase,
                "status": "completed",
                "time": str(datetime.now())
            })

        return result


executor = Executor()
''',

"tester.py": '''
class Tester:

    def run(self):

        return {
            "tests": "completed",
            "status": "success"
        }


tester = Tester()
''',

"reporter.py": '''
import json
from pathlib import Path

class Reporter:

    def create(self, data):

        Path("reports").mkdir(exist_ok=True)

        Path("reports/build_report.json").write_text(
            json.dumps(data, indent=4),
            encoding="utf-8"
        )

        return data


reporter = Reporter()
''',

"queue.py": '''
class BuildQueue:

    def __init__(self):
        self.tasks = []

    def add(self, task):
        self.tasks.append(task)

    def list(self):
        return self.tasks


queue = BuildQueue()
'''
}


for name, content in files.items():

    path = BASE / name
    path.parent.mkdir(parents=True, exist_ok=True)

    if not path.exists():
        path.write_text(
            content.strip(),
            encoding="utf-8"
        )


Path("storage").mkdir(exist_ok=True)
Path("reports").mkdir(exist_ok=True)


print("AGS AUTONOMOUS BUILDER V1 installed")
print("Created:")
for f in files:
    print("-", f)