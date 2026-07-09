from app.ai.orchestrator.runtime.runtime import OrchestratorRuntime


class WorkflowExecutor:

    def __init__(self):

        self.runtime = OrchestratorRuntime()


    def execute(self, workflow):

        self.runtime.start(
            {
                "workflow": workflow.name
            }
        )

        results = []

        try:

            for step in workflow.steps:

                step.start()

                result = {

                    "step": step.name,

                    "agent": step.agent,

                    "action": step.action,

                    "status": "completed"

                }

                step.finish()

                results.append(result)


            self.runtime.finish()


        except Exception as e:

            self.runtime.fail(e)


        return {

            "workflow": workflow.name,

            "steps": results,

            "runtime": self.runtime.report()

        }
