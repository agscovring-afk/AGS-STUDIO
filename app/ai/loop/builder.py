class BuildStep:

    def run(self, data):

        return {
            "step":"BUILD",
            "input":data,
            "status":"DONE"
        }


builder = BuildStep()
