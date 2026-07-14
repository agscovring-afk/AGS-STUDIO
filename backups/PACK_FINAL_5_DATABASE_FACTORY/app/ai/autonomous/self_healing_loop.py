from app.ai.autonomous.real_agent_bridge import real_agent_bridge


class SelfHealingLoop:

    def __init__(self):
        self.bridge = real_agent_bridge
        self.max_retries = 3


    def diagnose(self, result):

        print("[DIAGNOSIS]")

        if result.get("status") == "completed":

            return {
                "needs_fix": False,
                "message": "Execution healthy"
            }


        return {
            "needs_fix": True,
            "message": "Execution failed - repair required",
            "error": result.get("validation")
        }



    def repair(self, task, diagnosis):

        print("[REPAIR AGENT]")

        repair_result = {
            "status": "repair_attempted",
            "task": task,
            "diagnosis": diagnosis
        }

        return repair_result



    def execute(self, task):

        attempts = 0


        while attempts < self.max_retries:

            print(f"\n[SELF HEALING ATTEMPT {attempts + 1}]")


            result = self.bridge.execute(task)


            diagnosis = self.diagnose(result)


            if not diagnosis["needs_fix"]:

                return {
                    "status": "completed",
                    "attempts": attempts + 1,
                    "result": result
                }


            self.repair(task, diagnosis)

            attempts += 1



        return {
            "status": "failed",
            "message": "Self healing limit reached",
            "attempts": attempts
        }



self_healing_loop = SelfHealingLoop()
