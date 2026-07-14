class EngineBase:

    name = "ENGINE"

    def run(self, context):

        return {
            "engine": self.name,
            "status": "ready",
            "context": context
        }
