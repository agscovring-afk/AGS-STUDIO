from ags.ai.settings import AI_MODE


class PromptManager:

    def build(self, agent, task):

        if AI_MODE == "fast":

            return f"""
You are {agent}.
Give a short technical answer.
Focus only on the essential points.

Task:
{task}
"""

        else:

            return f"""
You are {agent}.
Provide a complete professional analysis.

Task:
{task}
"""
