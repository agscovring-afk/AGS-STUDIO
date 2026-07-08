from agents.architect import ArchitectAgent
from agents.backend import BackendAgent
from agents.database import DatabaseAgent
from agents.ui import UIAgent
from agents.testing import TestingAgent
from agents.documentation import DocumentationAgent


class AgentManager:


    def __init__(self):

        self.agents = {

            "architect":
                ArchitectAgent(),

            "backend":
                BackendAgent(),

            "database":
                DatabaseAgent(),

            "ui":
                UIAgent(),

            "testing":
                TestingAgent(),

            "documentation":
                DocumentationAgent()

        }


    def run(self, name, data):

        agent = self.agents.get(name)


        if not agent:

            return "Agent not found"


        return agent.analyze(data)
