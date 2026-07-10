from app.ai.autonomous.agent_router import router
from app.ai.autonomous.validator import validator


class ExecutionBridge:

    def __init__(self):
        self.router = router
        self.validator = validator


    def execute_task(self, task):

        print("\n[EXECUTION BRIDGE]")
        print(f"Task: {task.name}")

        # Route task to agent
        result = self.router.execute(task)

        print("[AGENT RESULT]")
        print(result)


        # Validate result
        validation = self.validator.validate(result)


        if not validation.get("success", False):

            print("[VALIDATION FAILED]")
            print(validation)

            return {
                "status": "failed",
                "task": task.name,
                "result": result,
                "validation": validation
            }


        print("[VALIDATION PASSED]")


        return {
            "status": "completed",
            "task": task.name,
            "result": result,
            "validation": validation
        }


execution_bridge = ExecutionBridge()