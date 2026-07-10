from app.ai.autonomous.workflow_executor import workflow_executor


class AutonomousRuntimeLoop:

    def __init__(self):
        self.executor = workflow_executor


    def run(self, plan):

        print("\n================================")
        print(" AUTONOMOUS RUNTIME LOOP V1")
        print("================================")

        print("[PLAN RECEIVED]")
        print(plan)

        runtime_state = {
            "status": "running",
            "plan": plan,
            "completed_tasks": []
        }


        workflow = plan.get("tasks", [])


        result = self.executor.run_workflow(workflow)


        runtime_state["completed_tasks"] = result
        runtime_state["status"] = "completed"


        print("\n[AUTONOMOUS LOOP COMPLETE]")

        return runtime_state


runtime_loop = AutonomousRuntimeLoop()
