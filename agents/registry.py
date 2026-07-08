from typing import Dict


class AgentRegistry:
    """
    Registry for AGS Agents.
    """

    def __init__(self):

        self.agents: Dict = {}


    def register(
        self,
        agent
    ):

        name = agent.name

        self.agents[name] = agent


    def get(
        self,
        name
    ):

        return self.agents.get(
            name
        )


    def list_agents(
        self
    ):

        return list(
            self.agents.keys()
        )


    def describe(
        self
    ):

        return {

            name:
                agent.info()

            for name, agent
            in self.agents.items()

        }


agent_registry = AgentRegistry()