
from app.ai.autonomous.decision_integration import decision_integration
from app.ai.autonomous.real_agent_bridge import real_agent_bridge


class AutonomousTaskOrchestrator:


    def __init__(self):

        self.decision = decision_integration
        self.bridge = real_agent_bridge



    def execute_request(self, request):

        print("\n================================")
        print(" AUTONOMOUS TASK ORCHESTRATOR V2")
        print("================================")


        plan = self.decision.build_plan(request)


        results = []


        for task in plan.get("tasks", []):

            print("\n[TASK DISPATCH]")
            print(task["name"])

            results.append(
                self.bridge.execute(task)
            )


        return {

            "request": request,
            "plan": plan,
            "results": results

        }



task_orchestrator = AutonomousTaskOrchestrator()
