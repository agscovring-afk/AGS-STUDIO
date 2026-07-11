from app.ai.autonomous.agents.architect_agent import ArchitectAgent

try:
    from agents.backend import BackendAgent
    from agents.database import DatabaseAgent
    from agents.ui import UIAgent
    from agents.testing import TestingAgent
    from agents.documentation import DocumentationAgent
    from app.ai.autonomous.workers.module_builder_worker import ModuleBuilderWorker

    BuildAgent = ModuleBuilderWorker

except Exception:
    BackendAgent = None
    DatabaseAgent = None
    UIAgent = None
    TestingAgent = None
    DocumentationAgent = None
    BuildAgent = None


class AgentRegistry:

    def __init__(self):
        self.agents = {}


    def register(self, name, agent):
        self.agents[name] = agent


    def get(self, name):
        return self.agents.get(name)


    def list_agents(self):
        return list(self.agents.keys())


    def execute(self, name, task):

        agent = self.get(name)

        if agent is None:
            return {
                "status": "missing",
                "agent": name
            }


        if hasattr(agent, "execute"):

            if name == "BUILD_AGENT" and isinstance(task, str):

                task = {
                    "module": task.replace(" ", "_").lower(),
                    "request": task
                }

            return agent.execute(task)


        if hasattr(agent, "analyze"):
            return agent.analyze(task)


        return {
            "status": "unknown",
            "agent": name
        }



class DefaultAgent:

    def __init__(self, name):
        self.name = name


    def execute(self, task):

        return {
            "status": "completed",
            "agent": self.name,
            "task": task
        }



registry = AgentRegistry()


registry.register(
    "ARCHITECT_AGENT",
    ArchitectAgent(".")
)


AGENT_MAP = {

    "DATABASE_AGENT": DatabaseAgent,
    "BACKEND_AGENT": BackendAgent,
    "UI_AGENT": UIAgent,
    "TESTING_AGENT": TestingAgent,
    "DOCUMENTATION_AGENT": DocumentationAgent,
    "BUILD_AGENT": BuildAgent

}


for name, agent_class in AGENT_MAP.items():

    if agent_class:

        registry.register(
            name,
            agent_class()
        )

    else:

        registry.register(
            name,
            DefaultAgent(name)
        )
