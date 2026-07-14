
from enterprise_builder.core.autonomous_repair_loop import AutonomousRepairLoop


class RepairManager:


    def __init__(
        self,
        validator,
        healing_engine,
        repair_planner,
        fixer_engine
    ):

        self.loop = AutonomousRepairLoop(
            validator,
            healing_engine,
            repair_planner,
            fixer_engine
        )


    def execute(self, target="."):

        return self.loop.run(
            target
        )
