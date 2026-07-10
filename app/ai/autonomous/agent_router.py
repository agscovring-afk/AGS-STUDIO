
from app.ai.autonomous.agent_registry import registry



class AgentRouter:


    def __init__(self):

        self.registry = registry



    def execute(self, task):

        if isinstance(task, dict):

            agent_name = task.get(
                "agent",
                "ARCHITECT_AGENT"
            )

        else:

            agent_name = "ARCHITECT_AGENT"



        agent = self.registry.get(agent_name)


        if not agent:

            return {

                "status": "no_agent",

                "agent": agent_name,

                "task": task

            }



        return agent.execute(task)




router = AgentRouter()
