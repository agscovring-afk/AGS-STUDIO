from enterprise_builder.core.ai_activation import EnterpriseAIActivation
from enterprise_builder.planner.enterprise_planner import EnterprisePlanner


class AGSEnterpriseAIPlugin:


    def __init__(self):

        self.engine = EnterpriseAIActivation()

        self.planner = EnterprisePlanner()



    def ask(self, request):

        blueprint = self.planner.analyze(
            request
        )


        result = self.engine.handle_request(
            request
        )


        print(
            "AGS ENTERPRISE AI EXECUTION"
        )


        print(
            "ENTERPRISE BLUEPRINT GENERATED"
        )


        print(
            blueprint
        )


        print(result)


        return {
            "request": request,
            "blueprint": blueprint,
            "execution": result
        }
