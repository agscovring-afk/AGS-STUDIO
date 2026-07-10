from .architect_agent import ArchitectAgent
from .database_agent import DatabaseAgent
from .backend_agent import BackendAgent
from .ui_agent import UIAgent
from .testing_agent import TestingAgent
from .documentation_agent import DocumentationAgent


class AgentLoader:

    def __init__(self):
        self.agents = {}
        self.load_default_agents()

    def register(self, agent_class):

        agent = agent_class()

        self.agents[agent.name] = agent

        return agent


    def load_default_agents(self):

        self.register(ArchitectAgent)
        self.register(DatabaseAgent)
        self.register(BackendAgent)
        self.register(UIAgent)
        self.register(TestingAgent)
        self.register(DocumentationAgent)


    def get_agent(self, name):

        return self.agents.get(name)


    def list_agents(self):

        return list(self.agents.keys())


    def run_agent(self, name, task):

        agent = self.get_agent(name)

        if not agent:

            return {
                "status": "error",
                "message": f"Agent {name} not found"
            }

        return agent.run(task)