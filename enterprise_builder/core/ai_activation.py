from enterprise_builder.core.master_agent_bridge import MasterAgentEnterpriseBridge


class EnterpriseAIActivation:


    def __init__(self):

        self.bridge = MasterAgentEnterpriseBridge()



    def handle_request(self, request):

        return self.bridge.process(
            request
        )