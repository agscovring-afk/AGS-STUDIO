class TaskRouter:


    def route(self, analysis):

        return {
            "route": "AGENT_PIPELINE",
            "task": analysis["request"]
        }


router = TaskRouter()
