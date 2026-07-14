from .base_agent import BaseAgent


class BackendAgent(BaseAgent):

    name = "backend_agent"
    role = "backend developer"

    def analyze(self, task):
        self.log("Analyzing backend logic")

        return {
            "agent": self.name,
            "task": task,
            "focus": "backend"
        }