class AILayoutPlanner:

    def process(self, context):

        context["layout"] = {
            "type": "responsive",
            "structure": "generated"
        }

        return context
