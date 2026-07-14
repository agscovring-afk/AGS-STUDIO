from enterprise_builder.core.enterprise_pipeline import EnterprisePipeline


class EnterpriseAutonomousBridge:


    def __init__(self):

        self.pipeline = EnterprisePipeline()



    def execute_task(self, task):

        if "enterprise" in task.lower() or "erp" in task.lower():

            return self.pipeline.execute(
                "AGS_AI_ENTERPRISE"
            )


        return {
            "status":"IGNORED",
            "task":task
        }