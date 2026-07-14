from enterprise_builder.core.enterprise_pipeline import EnterprisePipeline


class EnterpriseAutonomousBridge:


    def __init__(self):

        self.pipeline = EnterprisePipeline()


    def execute_task(self, task):

        request = str(task).lower()


        if (
            "enterprise" in request
            or "erp" in request
            or "system" in request
            or "software" in request
        ):

            return self.pipeline.execute(
                "AGS_AI_ENTERPRISE"
            )


        return self.pipeline.execute(
            "AGS_AI_ENTERPRISE"
        )