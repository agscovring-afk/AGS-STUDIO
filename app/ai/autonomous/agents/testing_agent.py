from .base_agent import BaseAgent


class TestingAgent(BaseAgent):

    name = "testing_agent"
    role = "quality assurance"

    def analyze(self, task):
        self.log("Preparing tests")

        return {
            "agent": self.name,
            "task": task,
            "focus": "testing"
        }