class Planner:

    def plan(self, request):

        return {
            "request": request,
            "phases": [
                "Analyze requirements",
                "Design architecture",
                "Generate modules",
                "Run tests",
                "Create report"
            ]
        }


planner = Planner()