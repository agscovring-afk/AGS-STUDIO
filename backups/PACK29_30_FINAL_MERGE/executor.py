from app.ai.autonomous.execution_bridge import execution_bridge
from app.ai.memory.knowledge_store import store as knowledge_store
from app.ai.intelligence.module_builder.autonomous_module_builder import AutonomousModuleBuilder


class TaskExecutor:


    def __init__(self, context=None):

        self.context = context
        self.bridge = execution_bridge
        self.module_builder = AutonomousModuleBuilder()



    def execute(self, task):


        builder_result = None


        try:

            builder_result = self.module_builder.build(
                task.description
                if hasattr(task, "description")
                else task.name
            )

        except Exception:

            builder_result = None



        result = self.bridge.execute_task(task)



        if builder_result:

            result["module_builder"] = builder_result



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
