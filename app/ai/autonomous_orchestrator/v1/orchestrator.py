class AutonomousOrchestrator:

    def execute(self, engine, request):

        workflow = {
            "state": "RUNNING",
            "request": request
        }

        result = engine.run(request)

        workflow["state"] = "SUCCESS"
        workflow["result"] = result

        return workflow
