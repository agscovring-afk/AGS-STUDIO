from agents.base_agent import AIEnabledAgent


class ArchitectAgent(AIEnabledAgent):

    name = "architect"


    def __init__(self):

        super().__init__(self.name)


    def analyze(self, module, session=None):

        ai_result = self.ask_ai(
            f"Analyze architecture for {module}",
            session
        )

        return {
            "module": module,
            "status": "analyzed",
            "ai": ai_result
        }
