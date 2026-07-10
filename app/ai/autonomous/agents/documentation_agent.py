from .base_agent import BaseAgent


class DocumentationAgent(BaseAgent):

    name = "documentation_agent"
    role = "documentation writer"

    def analyze(self, task):
        self.log("Creating documentation plan")

        return {
            "agent": self.name,
            "task": task,
            "focus": "documentation"
        }