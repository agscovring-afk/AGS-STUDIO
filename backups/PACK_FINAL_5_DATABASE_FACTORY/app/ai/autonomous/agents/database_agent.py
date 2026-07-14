from .base_agent import BaseAgent


class DatabaseAgent(BaseAgent):

    name = "database_agent"
    role = "database designer"

    def analyze(self, task):
        self.log("Analyzing database requirements")

        return {
            "agent": self.name,
            "task": task,
            "focus": "database"
        }
