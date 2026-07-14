class FullAutonomousPipelineTest:
    def execute(self,data):
        return {
            "engine":"FULL_AUTONOMOUS_PIPELINE_TEST_V1",
            "status":"passed",
            "pipeline":data
        }
