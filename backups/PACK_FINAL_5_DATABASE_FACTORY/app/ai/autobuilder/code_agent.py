from app.ai.autobuilder.schema_generator import schema_generator
from app.ai.autobuilder.module_generator import module_generator


class CodeAgent:

    def build(self, request):

        schema = schema_generator.generate(
            request
        )

        path = module_generator.generate(
            schema
        )

        return {
            "schema": schema,
            "generated": path
        }


code_agent = CodeAgent()