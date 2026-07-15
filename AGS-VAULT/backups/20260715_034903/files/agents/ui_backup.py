from agents.base_agent import AIEnabledAgent


class UIAgent(AIEnabledAgent):


    name = "ui"


    def __init__(self):

        super().__init__(self.name)


    def analyze(self, module, session=None):

        return {

            "agent": self.name,

            "module": module,

            "ai":
                self.ask_ai(
                    f"Design UI for {module}"
                )

        }
