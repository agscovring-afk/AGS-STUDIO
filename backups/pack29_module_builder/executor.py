from app.ai.autonomous.execution_bridge import execution_bridge
from app.ai.memory.knowledge_store import store as knowledge_store


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


        knowledge_store.store_execution(
            task.name,
            result
        )


        return result
