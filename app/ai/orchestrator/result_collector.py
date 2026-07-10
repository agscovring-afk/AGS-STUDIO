class ResultCollector:


    def collect(self, results):

        return {
            "status":
            "COMPLETED",
            "results":
            results
        }


collector = ResultCollector()
