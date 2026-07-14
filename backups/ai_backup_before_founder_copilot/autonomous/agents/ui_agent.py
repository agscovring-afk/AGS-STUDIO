from .base_agent import BaseAgent


class UIAgent(BaseAgent):

    name = "ui_agent"
    role = "user interface developer"

    def analyze(self, task):
        self.log("Analyzing UI requirements")

        return {
            "agent": self.name,
            "task": task,
            "focus": "ui"
        }