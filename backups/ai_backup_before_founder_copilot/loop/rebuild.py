class RebuildStep:

    def run(self, data):

        return {
            "step":"REBUILD",
            "status":"COMPLETED"
        }


rebuild = RebuildStep()
