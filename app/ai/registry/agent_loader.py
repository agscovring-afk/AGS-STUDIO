from app.ai.registry.agent_registry import registry


class AgentLoader:


    def load(self,name):

        agent = registry.get(name)

        if agent:
            return {
                "status":"LOADED",
                "agent":name
            }

        return {
            "status":"NOT_FOUND",
            "agent":name
        }


loader = AgentLoader()
