from app.ai.autonomous.execution_bridge import execution_bridge


class TaskExecutor:

    def __init__(self, context=None):
        self.context = context
        self.bridge = execution_bridge

    def execute(self, task):

        result = self.bridge.execute_task(task)

        if result.get("status") == "completed":
            if hasattr(task, "status"):
                try:
                    from app.ai.autonomous.models import TaskStatus
                    task.status = TaskStatus.COMPLETED
                except Exception:
                    pass
        else:
            if hasattr(task, "status"):
                try:
                    from app.ai.autonomous.models import TaskStatus
                    task.status = TaskStatus.FAILED
                except Exception:
                    pass

        task.result = result

        return result
