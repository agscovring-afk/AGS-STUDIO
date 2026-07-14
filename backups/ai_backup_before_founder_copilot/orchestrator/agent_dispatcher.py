from app.ai.registry.agent_registry import registry


class AgentDispatcher:


    def dispatch(self, agent_name, task):

        agent = registry.get(agent_name)

        if agent:

            return agent.execute(task)


        return {
            "error": "AGENT_NOT_FOUND"
        }


dispatcher = AgentDispatcher()
