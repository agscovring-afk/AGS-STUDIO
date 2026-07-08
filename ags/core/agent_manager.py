from agents.architect import ArchitectAgent
from agents.backend import BackendAgent
from agents.database import DatabaseAgent
from agents.ui import UIAgent
from agents.testing import TestingAgent
from agents.documentation import DocumentationAgent

from app.ai.providers.provider_manager import ProviderManager



class AgentManager:


    def __init__(self):

        self.provider_manager = ProviderManager()


        self.agents = {

            "architect": ArchitectAgent(),
            "backend": BackendAgent(),
            "database": DatabaseAgent(),
            "ui": UIAgent(),
            "testing": TestingAgent(),
            "documentation": DocumentationAgent()

        }



    def run(self, name, module, session=None):

        agent = self.agents.get(name)


        if not agent:

            raise Exception(
                f"Agent {name} not found"
            )


        provider = self.provider_manager.get()


        if hasattr(agent, "set_provider"):

            agent.set_provider(
                provider
            )


        return agent.analyze(
            module,
            session
        )