from app.ai.autonomous.task_orchestrator import task_orchestrator
from app.ai.autonomous.self_healing_loop import self_healing_loop
from app.ai.autonomous.build_report import build_report


class FullAutonomousMasterRuntime:

    def __init__(self):
        self.orchestrator = task_orchestrator
        self.healing = self_healing_loop
        self.report = build_report


    def run(self, request):

        print("\n================================")
        print(" AGS AUTONOMOUS MASTER RUNTIME V2")
        print("================================")


        print("[REQUEST]")
        print(request)


        execution = self.orchestrator.execute_request(request)


        report = self.report.generate({
            "status": "completed",
            "request": request,
            "execution": execution
        })


        print("\n[MASTER RUNTIME COMPLETE]")


        return {
            "system": "AGS AUTONOMOUS V2",
            "request": request,
            "execution": execution,
            "report": report
        }



master_runtime = FullAutonomousMasterRuntime()
