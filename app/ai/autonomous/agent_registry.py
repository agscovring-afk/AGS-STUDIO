
class AgentRegistry:


    def __init__(self):

        self.agents = {}



    def register(self, name, agent):

        self.agents[name] = agent



    def get(self, name):

        return self.agents.get(name)



    def list_agents(self):

        return list(self.agents.keys())




class DefaultAgent:


    def __init__(self, name):

        self.name = name



    def execute(self, task):

        return {

            "status": "completed",

            "agent": self.name,

            "task": task,

            "message": f"{self.name} executed task"

        }



registry = AgentRegistry()


for agent_name in [

    "ARCHITECT_AGENT",
    "DATABASE_AGENT",
    "BACKEND_AGENT",
    "UI_AGENT",
    "TESTING_AGENT"

]:

    registry.register(
        agent_name,
        DefaultAgent(agent_name)
    )
