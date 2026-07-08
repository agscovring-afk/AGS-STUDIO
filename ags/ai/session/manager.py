from ags.ai.hub import AIHub
from ags.ai.session.session import AISession


class AISessionManager:


    def __init__(self):

        self.ai = AIHub()



    def create(self, module):

        return AISession(module)



    def analyze(self, session):

        prompt = f"""
Analyze the software module: {session.module}

Create a compact technical plan including:

1. Architecture
2. Database design
3. Backend structure
4. UI structure
5. Testing strategy
6. Documentation plan

Return a structured technical response.
"""


        result = self.ai.ask(prompt)


        session.context["main_analysis"] = result


        return session
