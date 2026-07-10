from app.ai.orchestrator.orchestrator import orchestrator


class AgentFlow:


    def execute(self, task):

        return orchestrator.run(task)


flow = AgentFlow()
