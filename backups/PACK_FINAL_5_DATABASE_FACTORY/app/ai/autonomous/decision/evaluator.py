class TaskEvaluator:


    def evaluate(self, task):

        task_lower = task.lower()

        category = "GENERAL"

        if "architecture" in task_lower or "design" in task_lower:
            category = "ARCHITECTURE"

        elif "database" in task_lower or "schema" in task_lower:
            category = "DATABASE"

        elif "ui" in task_lower or "interface" in task_lower:
            category = "UI"

        elif "code" in task_lower or "backend" in task_lower:
            category = "BACKEND"


        return {
            "category": category,
            "complexity": "HIGH",
            "priority": 10
        }


evaluator = TaskEvaluator()