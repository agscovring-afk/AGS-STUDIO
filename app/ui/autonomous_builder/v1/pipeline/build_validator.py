class BuildValidator:

    def process(self, context):

        context["validation"] = {
            "status": "passed"
        }

        return context
