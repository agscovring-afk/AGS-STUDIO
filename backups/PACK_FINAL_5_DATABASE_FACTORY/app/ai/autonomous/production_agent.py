
from app.ai.autonomous.real_agent_engine import real_agent_engine


class ProductionAgent:


    def __init__(self,name):

        self.name=name



    def execute(self,task):

        return real_agent_engine.execute(
            self.name,
            task
        )
