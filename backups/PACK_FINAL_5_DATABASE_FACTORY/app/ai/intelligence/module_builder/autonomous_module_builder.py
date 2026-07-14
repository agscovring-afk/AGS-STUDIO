from .construction_module_planner import ConstructionModulePlanner
from app.ai.autobuilder.module_generator import module_generator


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



    def build(self, task):

        plan = self.build_plan(task)


        generated = []


        for module in plan["modules"]:


            schema = {

                "module": module,

                "tables": [
                    module
                ]

            }


            try:

                path = module_generator.generate(
                    schema
                )


                generated.append(
                    {
                        "module": module,
                        "path": path,
                        "status": "generated"
                    }
                )


            except Exception as e:


                generated.append(
                    {
                        "module": module,
                        "error": str(e)
                    }
                )


        return {

            "plan": plan,

            "generated": generated

        }
