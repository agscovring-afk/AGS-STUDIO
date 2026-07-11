"""
AGS Autonomous Runtime V3

Full Runtime:
Kernel + Memory + Orchestrator + Pipeline
"""

from app.ai.autonomous.kernel import kernel
from app.ai.autonomous.memory.memory import memory
from app.ai.autonomous.orchestrator.orchestrator import orchestrator


class AutonomousRuntime:

    def __init__(self):

        self.kernel = kernel
        self.memory = memory
        self.orchestrator = orchestrator


    def start(self):

        return self.kernel.start()


    def execute(self, request):

        self.memory.remember(
            "last_request",
            {
                "request": request,
                "system": "AGS AUTONOMOUS CORE V3"
            },
            "AUTONOMOUS"
        )


        result = self.orchestrator.execute(
            request
        )


        self.memory.remember(
            "last_result",
            result,
            "AUTONOMOUS"
        )


        return {

            "system":
            "AGS AUTONOMOUS V3",

            "mode":
            "FULL ORCHESTRATOR RUNTIME",

            "request":
            request,

            "result":
            result

        }


autonomous = AutonomousRuntime()