from ags.core.agent_manager import AgentManager
from app.ai.router.ai_router import ai_router


class MasterAgent:

    def __init__(self):

        self.manager = AgentManager()

        ai_router.set_default(
            "ollama"
        )


    def ask(self, request):

        print("\n================================")
        print(" AGS MASTER AI - ROUTER MODE")
        print("================================")

        print("Request:", request)


        context_prompt = f"""
You are AGS-STUDIO MASTER AI.

Project:
AGS ERP Construction Platform.

User Request:
{request}

Analyze professionally.

Return:
- Architecture
- Database design
- Backend modules
- UI design
- Required agents tasks
- Implementation steps
"""


        print("\nMASTER AI thinking...")


        result = ai_router.route(
            context_prompt,
            memory_key="AGS"
        )


        print("\n================================")
        print(" MASTER RESPONSE COMPLETE")
        print("================================")


        return result
