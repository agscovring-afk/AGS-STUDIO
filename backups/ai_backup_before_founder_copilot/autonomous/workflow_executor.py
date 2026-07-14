from app.ai.autonomous.execution_bridge import execution_bridge


class WorkflowExecutor:

    def __init__(self):
        self.bridge = execution_bridge


    def run_workflow(self, workflow):

        print("\n================================")
        print(" WORKFLOW EXECUTOR V1")
        print("================================")

        results = []

        for task in workflow:

            print(f"\n[TASK START] {task.name}")

            result = self.bridge.execute_task(task)

            results.append(result)

            print(f"[TASK END] {task.name}")


        print("\n[WORKFLOW COMPLETE]")

        return {
            "status": "completed",
            "tasks": len(results),
            "results": results
        }


workflow_executor = WorkflowExecutor()
