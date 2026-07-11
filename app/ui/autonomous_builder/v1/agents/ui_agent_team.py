class UIAgentTeam:

    def __init__(self):

        self.agents = [
            "UI_ARCHITECT",
            "UI_DESIGNER",
            "UI_DEVELOPER",
            "UI_TESTER"
        ]


    def run(self,task):

        return {
            "task":task,
            "agents":self.agents,
            "status":"completed"
        }
