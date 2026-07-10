"""
AGS Autonomous V2
Autonomous Pipeline V3

Engine -> Planner -> Router V2 -> Agent -> Executor -> Validator -> Report
"""

from datetime import datetime


class AutonomousPipeline:


    def __init__(
        self,
        engine=None,
        planner=None,
        router=None,
        executor=None,
        validator=None
    ):

        self.engine = engine
        self.planner = planner
        self.router = router
        self.executor = executor
        self.validator = validator

        self.history = []



    def run(self, task):

        report = {
            "task": getattr(task, "name", str(task)),
            "started": datetime.now().isoformat(),
            "steps": [],
            "status": "RUNNING"
        }


        try:

            # ENGINE

            report["steps"].append(
                "ENGINE_ANALYSIS"
            )

            if self.engine:

                analysis = self.engine.analyze(
                    task
                )

            else:

                analysis = task



            # PLANNER

            report["steps"].append(
                "TASK_PLANNING"
            )

            if self.planner:

                plan = self.planner.create_plan(
                    analysis
                )

            else:

                plan = analysis



            # ROUTER V2

            report["steps"].append(
                "AGENT_ROUTING"
            )

            agent = None


            if self.router:

                try:

                    agent = self.router.resolve(
                        plan
                    )

                except Exception as e:

                    report["router_error"] = str(e)



            # EXECUTION

            report["steps"].append(
                "AGENT_EXECUTION"
            )


            if agent:

                result = agent.execute(
                    plan
                )


            elif self.router:

                result = self.router.execute(
                    plan
                )


            elif self.executor:

                result = self.executor.execute(
                    plan
                )


            else:

                result = {
                    "message": "No execution provider"
                }



            # VALIDATION V3

            report["steps"].append(
                "VALIDATION"
            )


            if self.validator:

                validation = self.validator.validate(
                    task,
                    result
                )

            else:

                validation = {
                    "valid": True
                }



            report["result"] = result
            report["validation"] = validation
            report["status"] = "COMPLETED"



        except Exception as e:

            report["status"] = "FAILED"
            report["error"] = str(e)



        report["finished"] = datetime.now().isoformat()


        self.history.append(
            report
        )


        return report