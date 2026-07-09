from typing import Dict

from agents.registry import agent_registry
from app.ai.memory.memory_service import memory_service


class AgentManager:
    """
    Runtime manager for AGS agents.
    """

    def __init__(self):

        self.registry = agent_registry
        self.memory = memory_service


    # ==========================
    # Register
    # ==========================

    def register(
        self,
        agent
    ):

        self.registry.register(
            agent
        )

        self.memory.remember_agent(
            agent.name,
            "Agent registered"
        )


    # ==========================
    # Get
    # ==========================

    def get(
        self,
        name
    ):

        return self.registry.get(
            name
        )


    # ==========================
    # Execute
    # ==========================

    def execute(
        self,
        agent_name,
        task,
        **kwargs
    ):

        agent = self.get(
            agent_name
        )

        if not agent:
            raise Exception(
                f"Agent not found: {agent_name}"
            )


        self.memory.remember_agent(
            agent_name,
            {
                "task": task,
                "status": "started"
            }
        )


        result = agent.run(
            task,
            **kwargs
        )


        self.memory.remember_agent(
            agent_name,
            {
                "task": task,
                "status": "completed",
                "result": result
            }
        )


        return result


    # ==========================
    # Status
    # ==========================

    def status(
        self
    ) -> Dict:

        return {
            "agents":
                self.registry.describe()
        }


agent_manager = AgentManager()