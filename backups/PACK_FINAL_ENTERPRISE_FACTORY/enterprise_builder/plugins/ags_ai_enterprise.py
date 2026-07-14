from enterprise_builder.core.ai_activation import EnterpriseAIActivation


class AGSEnterpriseAIPlugin:


    def __init__(self):

        self.engine = EnterpriseAIActivation()



    def ask(self, request):

        result = self.engine.handle_request(
            request
        )

        print(
            "AGS ENTERPRISE AI EXECUTION"
        )

        print(result)

        return result