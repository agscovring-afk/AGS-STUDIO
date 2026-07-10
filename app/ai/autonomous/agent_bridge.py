"""
AGS Autonomous V2
Agent Bridge V2
"""


from app.ai.autobuilder.code_agent import code_agent

from .agent_registry import registry
from .agent_router import router



#
# Register Agents
#

registry.register(
    "code",
    code_agent
)



class AgentBridge:


    def execute(self, task):

        return router.execute(task)



agent_bridge = AgentBridge()