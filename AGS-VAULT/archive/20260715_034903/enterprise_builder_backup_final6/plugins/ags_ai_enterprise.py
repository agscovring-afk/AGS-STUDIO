from enterprise_builder.core.ai_activation import EnterpriseAIActivation
from enterprise_builder.planner.enterprise_planner import EnterprisePlanner
from enterprise_builder.metadata.enterprise_metadata_generator import EnterpriseMetadataGenerator
from enterprise_builder.generators.code.code_factory import CodeFactory
from enterprise_builder.database.database_factory import DatabaseFactory


class AGSEnterpriseAIPlugin:


    def __init__(self):

        self.engine = EnterpriseAIActivation()

        self.planner = EnterprisePlanner()

        self.metadata = EnterpriseMetadataGenerator()

        self.code_factory = CodeFactory()

        self.database_factory = DatabaseFactory()



    def ask(self, request):

        blueprint = self.planner.analyze(
            request
        )


        metadata = self.metadata.generate(
            blueprint
        )


        generated_database = self.database_factory.build(
            metadata
        )


        generated_code = self.code_factory.generate(
            metadata
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
            "ENTERPRISE DATABASE GENERATED"
        )

        print(
            generated_database
        )


        print(
            "ENTERPRISE CODE GENERATED"
        )


        print(
            {
                "models": len(generated_code),
                "repositories": len(generated_code),
                "services": len(generated_code),
                "controllers": len(generated_code)
            }
        )


        print(result)


        return {
            "request": request,
            "blueprint": blueprint,
            "metadata": metadata,
            "database": generated_database,
            "code": generated_code,
            "execution": result
        }
