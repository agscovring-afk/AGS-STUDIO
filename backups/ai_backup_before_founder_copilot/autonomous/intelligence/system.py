from app.ai.autonomous.decision import decision_engine
from app.ai.autonomous.memory import memory
from app.ai.autonomous.planner import planner
from app.ai.autonomous.workflow import workflow_engine


class IntelligenceSystem:


    def run(self, request):

        decision = decision_engine.decide(request)

        memory.remember(
            request,
            decision,
            "DECISION"
        )

        plan = planner.create_plan(
            request
        )

        workflow = workflow_engine.create(
            request,
            plan["steps"]
        )

        execution = workflow_engine.run(
            workflow
        )

        return {
            "system": "AGS AUTONOMOUS V2",
            "request": request,
            "decision": decision,
            "plan": plan,
            "workflow": execution,
            "status": "INTELLIGENCE PIPELINE ACTIVE"
        }



system = IntelligenceSystem()
