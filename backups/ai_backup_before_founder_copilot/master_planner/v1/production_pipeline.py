from app.ai.master_planner.v1 import (
    MasterPlanner,
    register_default_phases,
)

from ags.core.agent_manager import AgentManager
from ags.core.ai_orchestrator import AIOrchestrator


class ProductionPipeline:

    def __init__(self):

        self.manager = AgentManager()

        self.orchestrator = AIOrchestrator(
            self.manager
        )

        self.planner = MasterPlanner()

        self.registry = register_default_phases()

    def run(self):

        for phase in self.registry.all():

            self.planner.add_phase(
                phase.name
            )

            for task in phase.tasks:

                self.planner.add_task(
                    self.planner.phase(
                        phase.name
                    ),
                    task.name,
                    task.agent,
                    task.payload,
                )

        self.planner.register_agent(
            "architect",
            lambda task: self.orchestrator.run_team(
                task.name
            ),
        )

        report = self.planner.execute()

        self.planner.summary()

        return report
