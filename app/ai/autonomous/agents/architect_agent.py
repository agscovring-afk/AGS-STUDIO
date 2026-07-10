from .base_agent import BaseAgent


class ArchitectAgent(BaseAgent):

    name = "architect_agent"
    role = "system architecture designer"

    def analyze(self, task):
        self.log("Designing system architecture")

        return {
            "agent": self.name,
            "task": task,
            "focus": "architecture"
        }