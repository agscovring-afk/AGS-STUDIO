from enterprise_builder.core.enterprise_pipeline import EnterprisePipeline


class EnterpriseActionExecutor:


    def __init__(self):

        self.pipeline = EnterprisePipeline()


    def execute(self, task):

        name = getattr(task, "name", str(task))

        normalized = name.lower()


        actions = {

            "design_enterprise_architecture": "AGS_ARCHITECTURE",

            "create_erp_modules": "AGS_ERP_MODULES",

            "build_tenant_system": "AGS_MULTI_TENANT",

            "generate_enterprise_release": "AGS_RELEASE",

        }


        if name in actions:

            return self.pipeline.execute(
                actions[name]
            )


        if name == "validate_enterprise":

            return {
                "status": "validated",
                "task": name
            }


        construction_keywords = [

            "tender",
            "construction",
            "project",
            "projects",
            "inventory",
            "stock",
            "supplier",
            "suppliers",
            "erp",
            "enterprise"

        ]


        if any(
            keyword in normalized
            for keyword in construction_keywords
        ):

            return self.pipeline.execute(
                "AGS_CONSTRUCTION_ERP"
            )


        # Unknown actions are now resolved by Enterprise AI Pipeline
        return self.pipeline.execute(
            "AGS_AI_ENTERPRISE"
        )