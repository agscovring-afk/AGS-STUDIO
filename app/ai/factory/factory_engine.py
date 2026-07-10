class FactoryEngine:

    def build(self, request):

        return {
            "factory":
            "AGS FACTORY ENGINE",

            "request":
            request,

            "generated":[
                "DATABASE",
                "MODELS",
                "SERVICES",
                "CONTROLLERS",
                "UI",
                "REPORTS",
                "API",
                "TESTS",
                "DOCUMENTATION"
            ],

            "status":
            "BUILD_READY"
        }


factory = FactoryEngine()
