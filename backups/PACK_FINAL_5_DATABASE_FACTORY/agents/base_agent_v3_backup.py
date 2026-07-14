from ags.ai.hub import AIHub
from ags.ai.prompt_manager import PromptManager


class AIEnabledAgent:


    def __init__(self, name):

        self.name = name

        self.ai = AIHub()

        self.prompts = PromptManager()



    def ask_ai(self, task, session=None):


        if session and "main_analysis" in session.context:

            return {

                "provider": "session",

                "agent": self.name,

                "analysis": session.context["main_analysis"]

            }



        prompt = self.prompts.build(

            self.name,

            task

        )


        return self.ai.ask(prompt)
