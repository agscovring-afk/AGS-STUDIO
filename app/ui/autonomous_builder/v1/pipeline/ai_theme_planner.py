class AIThemePlanner:

    def process(self, context):

        context["theme"] = {
            "mode": "dark",
            "generated": True
        }

        return context
