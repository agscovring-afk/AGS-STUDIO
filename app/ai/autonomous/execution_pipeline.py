from app.ai.autonomous.runtime_loop import runtime_loop
from app.ai.autonomous.build_report import build_report


class AutonomousExecutionPipeline:

    def __init__(self):
        self.runtime = runtime_loop
        self.report = build_report


    def execute(self, plan):

        print("\n================================")
        print(" AGS AUTONOMOUS EXECUTION PIPELINE V1")
        print("================================")

        execution = self.runtime.run(plan)

        report = self.report.generate(execution)

        print("[EXECUTION PIPELINE COMPLETE]")

        return {
            "execution": execution,
            "report": report
        }


pipeline = AutonomousExecutionPipeline()
