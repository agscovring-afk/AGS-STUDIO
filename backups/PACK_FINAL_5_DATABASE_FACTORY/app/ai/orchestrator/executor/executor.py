from app.ai.orchestrator.core.workflow import Workflow


class WorkflowExecutor:

    def __init__(self):
        self.status = "ready"


    def execute(self, workflow: Workflow):

        results = []

        for step in workflow.steps:
            result = self.execute_step(step)
            results.append(result)

        return {
            "status": "completed",
            "results": results
        }


    def execute_step(self, step):

        return {
            "step": getattr(step, "name", "unknown"),
            "status": "done"
        }
