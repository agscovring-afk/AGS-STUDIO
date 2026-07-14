from enterprise_builder.core.enterprise_pipeline import EnterprisePipeline


class EnterpriseActionExecutor:


    def __init__(self):

        self.pipeline = EnterprisePipeline()


    def execute(self, task):

        name = getattr(task,"name",str(task))


        if name == "design_enterprise_architecture":

            return self.pipeline.execute(
                "AGS_ARCHITECTURE"
            )


        if name == "create_erp_modules":

            return self.pipeline.execute(
                "AGS_ERP_MODULES"
            )


        if name == "build_tenant_system":

            return self.pipeline.execute(
                "AGS_MULTI_TENANT"
            )


        if name == "generate_enterprise_release":

            return self.pipeline.execute(
                "AGS_RELEASE"
            )


        if name == "validate_enterprise":

            return {
                "status":"validated",
                "task":name
            }


        return {
            "status":"ignored",
            "task":name
        }