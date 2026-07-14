from .orchestrator import AutonomousOrchestrator


class AutonomousOrchestratorEngine:

    def __init__(self, core_engine=None):
        self.core_engine = core_engine
        self.orchestrator = AutonomousOrchestrator()

    def run(self, request):

        return self.orchestrator.execute(
            self.core_engine,
            request
        )
