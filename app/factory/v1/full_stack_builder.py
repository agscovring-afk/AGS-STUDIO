class FullStackAutonomousBuilder:

    def build(self, request):

        return {
            "database": True,
            "backend": True,
            "api": True,
            "ui": True,
            "tests": True,
            "request": request
        }
