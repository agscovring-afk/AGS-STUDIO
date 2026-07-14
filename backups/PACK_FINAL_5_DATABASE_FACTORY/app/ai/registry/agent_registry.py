from app.ai.agents.architect import agent as architect
from app.ai.agents.backend import agent as backend
from app.ai.agents.database import agent as database
from app.ai.agents.ui import agent as ui
from app.ai.agents.tester import agent as tester
from app.ai.agents.builder import agent as builder


class AgentRegistry:

    def __init__(self):

        self.agents = {
            "ARCHITECT_AGENT": architect,
            "BACKEND_AGENT": backend,
            "DATABASE_AGENT": database,
            "UI_AGENT": ui,
            "TESTER_AGENT": tester,
            "BUILDER_AGENT": builder
        }


    def get(self,name):

        return self.agents.get(name)


    def list_agents(self):

        return list(self.agents.keys())


registry = AgentRegistry()
