from app.ai.autonomous.kernel.kernel import kernel
from app.ai.autonomous.memory.memory import memory
from app.ai.autonomous.orchestrator.orchestrator import orchestrator

from app.ai.autonomous.pipeline import AutonomousPipeline
from app.ai.autonomous.engine_adapter import EngineAdapter
from app.ai.autonomous.master_bridge import MasterBridge


try:
    from app.ai.autonomous.executor import executor
except Exception:
    executor = None


try:
    from app.ai.autonomous.validator import AutonomousValidator
    validator = AutonomousValidator()
except Exception:
    validator = None



class AutonomousRuntime:


    def __init__(self):

        self.kernel = kernel
        self.memory = memory

        self.orchestrator = orchestrator

        self.executor = executor
        self.validator = validator


        self.pipeline = AutonomousPipeline(

            engine=self.orchestrator,
            planner=None,
            router=None,
            executor=self.executor,
            validator=self.validator

        )


        self.engine_adapter = EngineAdapter(

            self.orchestrator,
            self.pipeline

        )


        self.master = MasterBridge(

            engine_adapter=self.engine_adapter,
            router=None

        )



    def start(self):

        return self.kernel.start()



    def execute(self, request):

        self.memory.remember(

            {
                "request": request,
                "system": "AGS AUTONOMOUS CORE V3"

            }

        )


        result = self.orchestrator.execute(
            request
        )


        return {

            "system":
            "AGS AUTONOMOUS CORE V3",

            "kernel":
            self.kernel.status(),

            "request":
            request,

            "execution":
            result

        }



autonomous = AutonomousRuntime()
