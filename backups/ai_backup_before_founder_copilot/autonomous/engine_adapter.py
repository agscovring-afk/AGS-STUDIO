"""
AGS Autonomous V2
Engine Adapter V1

Connects Engine V2 with Autonomous Pipeline
"""

from datetime import datetime


class EngineAdapter:

    def __init__(self, engine, pipeline):
        self.engine = engine
        self.pipeline = pipeline


    def process(self, task):

        report = {
            "engine": "Engine V2 Adapter",
            "task": getattr(task, "name", str(task)),
            "started": datetime.now().isoformat()
        }

        try:

            # Send task through Engine V2
            if self.engine:
                prepared_task = self.engine.process(task)
            else:
                prepared_task = task


            # Execute Autonomous Pipeline
            result = self.pipeline.run(
                prepared_task
            )

            report["pipeline_result"] = result
            report["status"] = "COMPLETED"


        except Exception as e:

            report["status"] = "FAILED"
            report["error"] = str(e)


        report["finished"] = datetime.now().isoformat()

        return report