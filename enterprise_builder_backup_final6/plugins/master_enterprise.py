from enterprise_builder.core.master_agent_bridge import MasterAgentEnterpriseBridge
from enterprise_builder.core.production_guard import ProductionGuard


class MasterEnterprisePlugin:


    def __init__(self):

        self.bridge=MasterAgentEnterpriseBridge()

        self.guard=ProductionGuard()



    def execute(self, request):

        check=self.guard.check()


        if not check["ready"]:

            return {
                "status":"BLOCKED",
                "checks":check
            }


        return self.bridge.process(
            request
        )