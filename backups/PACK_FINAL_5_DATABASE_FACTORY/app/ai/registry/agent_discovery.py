from app.ai.registry.agent_registry import registry


class AgentDiscovery:


    def discover(self):

        return {
            "agents":
            registry.list_agents(),
            "count":
            len(registry.list_agents())
        }


discovery = AgentDiscovery()
