class PlanStep:

    def run(self, data):

        return {
            "step":"PLAN",
            "input":data,
            "status":"DONE"
        }


planner = PlanStep()
