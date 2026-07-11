"""
AGS Autonomous V2
Runtime V3

Full Component Wiring:
Router + Executor + Validator + Pipeline
"""

from app.ai.autonomous.pipeline import AutonomousPipeline
from app.ai.autonomous.engine_adapter import EngineAdapter
from app.ai.autonomous.master_bridge import MasterBridge


# Router V2

try:
    from app.ai.autonomous.agent_router import router

except Exception:
    router = None



# Executor V2

try:
    from app.ai.autonomous.executor import executor

except Exception:
    executor = None



# Validator Instance

try:
    from app.ai.autonomous.validator import AutonomousValidator

    validator = AutonomousValidator()

except Exception:
    validator = None



class AutonomousRuntime:


    def __init__(self):

        self.engine = None
        self.planner = None

        self.router = router
        self.executor = executor
        self.validator = validator


        self.pipeline = AutonomousPipeline(

            engine=self.engine,
            planner=self.planner,
            router=self.router,
            executor=self.executor,
            validator=self.validator

        )


        self.engine_adapter = EngineAdapter(

            self.engine,
            self.pipeline

        )


        self.master = MasterBridge(

            engine_adapter=self.engine_adapter,
            router=self.router

        )



    def execute(self, request):

        return self.master.execute_request(
            request
        )



# Global Runtime

autonomous = AutonomousRuntime()