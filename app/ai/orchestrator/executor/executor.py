from app.ai.orchestrator.runtime.runtime import OrchestratorRuntime
from app.ai.orchestrator.executor.agent_resolver import AgentResolver


class WorkflowExecutor:

    def __init__(self):

        self.runtime = OrchestratorRuntime()

        self.resolver = AgentResolver()


    def execute(self, workflow, module):

        self.runtime.start(
            {
                "workflow": workflow.name,
                "module": module
            }
        )

        results = []


        try:

            for step in workflow.steps:

                step.start()


                agent = self.resolver.resolve(
                    step.agent
                )


                output = agent.analyze(
                    module
                )


                step.finish()


                results.append({

                    "step": step.name,

                    "agent": step.agent,

                    "action": step.action,

                    "status": "completed",

                    "output": output

                })


            self.runtime.finish()


        except Exception as e:

            self.runtime.fail(e)

            results.append({

                "status": "failed",

                "error": str(e)

            })


        return {

            "workflow": workflow.name,

            "steps": results,

            "runtime": self.runtime.report()

        }
