from datetime import datetime


class BaseAgent:

    name = "base_agent"
    role = "generic autonomous agent"
    version = "1.0"

    def __init__(self, context=None):
        self.context = context or {}
        self.memory = []
        self.status = "initialized"

    def log(self, message):
        entry = {
            "time": datetime.now().isoformat(),
            "agent": self.name,
            "message": message
        }

        self.memory.append(entry)
        print(f"[{self.name.upper()}] {message}")

    def analyze(self, task):
        self.log(f"Analyzing task: {task}")

        return {
            "agent": self.name,
            "task": task,
            "analysis": "generic analysis"
        }

    def plan(self, task):
        self.log(f"Planning task: {task}")

        return {
            "steps": [
                "analyze",
                "execute",
                "validate"
            ]
        }

    def execute(self, task):
        self.log(f"Executing task: {task}")

        return {
            "status": "completed",
            "result": None
        }

    def validate(self, result):
        self.log("Validating result")

        return {
            "valid": True,
            "result": result
        }

    def run(self, task):

        self.status = "running"

        analysis = self.analyze(task)
        plan = self.plan(task)
        result = self.execute(task)
        validation = self.validate(result)

        self.status = "completed"

        return {
            "agent": self.name,
            "analysis": analysis,
            "plan": plan,
            "result": result,
            "validation": validation
        }