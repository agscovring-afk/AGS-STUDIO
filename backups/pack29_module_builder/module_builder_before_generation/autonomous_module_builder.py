from .construction_module_planner import ConstructionModulePlanner


class AutonomousModuleBuilder:


    def __init__(self):

        self.planner = ConstructionModulePlanner()


    def build_plan(self, task):

        modules = self.planner.plan(task)

        return {
            "task": task,
            "modules": modules,
            "architecture": [
                "metadata",
                "models",
                "repositories",
                "services",
                "controllers",
                "ui",
                "registry"
            ]
        }
