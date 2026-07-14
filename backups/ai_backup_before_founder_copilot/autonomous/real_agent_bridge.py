
from app.ai.autonomous.agent_router import router
from app.ai.autonomous.validator import validator



class RealAgentExecutionBridge:


    def __init__(self):

        self.router = router
        self.validator = validator



    def execute(self, task):

        print("\n================================")
        print(" REAL AGENT EXECUTION BRIDGE V2")
        print("================================")


        print("[TASK]")
        print(task)


        result = self.router.execute(task)


        print("[AGENT OUTPUT]")
        print(result)


        validation = self.validator.validate(result)


        if validation.get("success"):

            print("[VALIDATION PASSED]")

        else:

            print("[VALIDATION FAILED]")


        return {

            "status": "completed"
            if validation.get("success")
            else "failed",

            "task": task,
            "result": result,
            "validation": validation

        }



real_agent_bridge = RealAgentExecutionBridge()
