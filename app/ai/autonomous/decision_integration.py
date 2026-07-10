
from app.ai.autonomous.task_generator_intelligence import task_generator_intelligence


class DecisionIntegration:


    def __init__(self):

        self.generator = task_generator_intelligence



    def build_plan(self, request):

        print("\n[DECISION ENGINE]")

        tasks = self.generator.generate(request)


        decision = {

            "goal": request,
            "tasks": tasks

        }


        plan = {

            "name": "AGS AUTONOMOUS REAL PLAN",
            "request": request,
            "decision": decision,
            "tasks": tasks

        }


        print("[REAL TASK PLAN CREATED]")

        return plan



decision_integration = DecisionIntegration()
