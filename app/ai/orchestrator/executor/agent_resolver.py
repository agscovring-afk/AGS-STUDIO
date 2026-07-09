from ags.core.agent_manager import AgentManager


class AgentResolver:

    def __init__(self):

        self.manager = AgentManager()


    def resolve(self, agent_name):

        agent = self.manager.agents.get(
            agent_name
        )

        if agent is None:

            raise Exception(
                f"Agent {agent_name} not found"
            )

        return agent
