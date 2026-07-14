from datetime import datetime


class SharedTask:

    def __init__(self, name, description, priority=1):
        self.name = name
        self.description = description
        self.priority = priority
        self.status = "OPEN"
        self.assigned_to = None
        self.created_at = datetime.now().isoformat()

    def assign(self, agent):
        self.assigned_to = agent
        self.status = "ASSIGNED"

    def complete(self):
        self.status = "COMPLETED"


class TaskPool:

    def __init__(self):
        self.tasks = []

    def add(self, task):
        self.tasks.append(task)

    def pending(self):
        return [
            task for task in self.tasks
            if task.status != "COMPLETED"
        ]


task_pool = TaskPool()