from ags.ai.hub import AIHub
from ags.ai.prompt_manager import PromptManager


class AIEnabledAgent:

    def __init__(self, name):

        self.name = name
        self.ai = AIHub()
        self.prompts = PromptManager()


    def ask_ai(self, task):

        prompt = self.prompts.build(
            self.name,
            task
        )

        return self.ai.ask(prompt)
