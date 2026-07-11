class UIAssembler:

    def process(self, context):

        context["application_ui"] = {
            "layout": context.get("layout"),
            "components": context.get("components"),
            "theme": context.get("theme")
        }

        return context
