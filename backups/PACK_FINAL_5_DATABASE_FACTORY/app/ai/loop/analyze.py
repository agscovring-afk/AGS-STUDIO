class AnalyzeStep:

    def run(self, request):

        return {
            "step":"ANALYZE",
            "request":request,
            "status":"DONE"
        }


analyzer = AnalyzeStep()
