from agents.architect import ArchitectAgent
from agents.backend import BackendAgent
from agents.database import DatabaseAgent
from agents.ui import UIAgent
from agents.testing import TestingAgent
from agents.documentation import DocumentationAgent
from agents.build import BuildAgent

from app.ai.memory.memory_manager import MemoryManager
from app.ai.memory.memory_types import MemoryType


class AgentManager:

    def __init__(self):

        self.memory = MemoryManager()

        self.agents = {
            "architect": ArchitectAgent(),
            "backend": BackendAgent(),
            "database": DatabaseAgent(),
            "ui": UIAgent(),
            "testing": TestingAgent(),
            "documentation": DocumentationAgent(),
            "build": BuildAgent()
        }

    def list_agents(self):

        return list(self.agents.keys())

    def run(self, name, module, session=None):

        agent = self.agents.get(name)

        if agent is None:
            raise Exception(f"Agent {name} not found")

        result = agent.analyze(
            module,
            session
        )

        self.memory.remember(
            content=str(result),
            memory_type=MemoryType.AGENT,
            module=module,
            agent=name
        )

        return result


agent_manager = AgentManager()