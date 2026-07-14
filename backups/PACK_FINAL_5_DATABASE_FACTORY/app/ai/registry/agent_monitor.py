from app.ai.registry.agent_registry import registry


class AgentMonitor:


    def status(self):

        return {
            "system":
            "AGS AGENT MONITOR",
            "agents":
            registry.list_agents(),
            "status":
            "ACTIVE"
        }


monitor = AgentMonitor()
