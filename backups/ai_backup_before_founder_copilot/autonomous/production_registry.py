
from app.ai.autonomous.production_agent import ProductionAgent


class ProductionAgentRegistry:


    def __init__(self):

        self.agents = {

            "ARCHITECT_AGENT":
                ProductionAgent("ARCHITECT_AGENT"),

            "DATABASE_AGENT":
                ProductionAgent("DATABASE_AGENT"),

            "BACKEND_AGENT":
                ProductionAgent("BACKEND_AGENT"),

            "UI_AGENT":
                ProductionAgent("UI_AGENT"),

            "TESTING_AGENT":
                ProductionAgent("TESTING_AGENT")

        }



    def get(self,name):

        return self.agents.get(name)



production_registry = ProductionAgentRegistry()
