class AIComponentPlanner:

    def process(self, context):

        context["components"] = [
            "dashboard",
            "forms",
            "tables",
            "charts"
        ]

        return context
