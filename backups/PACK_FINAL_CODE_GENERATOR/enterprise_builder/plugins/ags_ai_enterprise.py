from enterprise_builder.core.ai_activation import EnterpriseAIActivation
from enterprise_builder.planner.enterprise_planner import EnterprisePlanner
from enterprise_builder.metadata.enterprise_metadata_generator import EnterpriseMetadataGenerator


class AGSEnterpriseAIPlugin:


    def __init__(self):

        self.engine = EnterpriseAIActivation()

        self.planner = EnterprisePlanner()

        self.metadata = EnterpriseMetadataGenerator()



    def ask(self, request):

        blueprint = self.planner.analyze(
            request
        )


        metadata = self.metadata.generate(
            blueprint
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


        print(
            "ENTERPRISE METADATA GENERATED"
        )


        print(
            metadata
        )


        print(
            result
        )


        return {
            "request": request,
            "blueprint": blueprint,
            "metadata": metadata,
            "execution": result
        }
