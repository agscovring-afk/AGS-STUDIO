class AgentResolver:

    def __init__(self):

        self.manager = None


    def _load_manager(self):

        if self.manager is None:

            from ags.core.agent_manager import AgentManager

            self.manager = AgentManager()


    def resolve(self, agent_name):

        self._load_manager()


        agent = self.manager.agents.get(
            agent_name
        )


        if agent is None:

            raise Exception(
                f"Agent {agent_name} not found"
            )


        return agent
