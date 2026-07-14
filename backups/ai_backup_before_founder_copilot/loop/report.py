class ReportStep:

    def run(self, data):

        return {
            "step":"REPORT",
            "result":data
        }


reporter = ReportStep()
