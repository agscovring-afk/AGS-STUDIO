
from app.ai.autonomous.production_registry import production_registry


class UltimateAgentBridge:


    def execute(self,task):


        agent_name = task.get(
            "agent"
        )


        agent = production_registry.get(
            agent_name
        )


        if not agent:

            return {

                "status":"no_agent",

                "agent":agent_name

            }



        result = agent.execute(
            task
        )


        return result



ultimate_bridge = UltimateAgentBridge()
