class DashboardGenerator:


    def generate(self, entity):

        return {
            "dashboard": f"{entity.name}_dashboard",
            "widgets": [
                "total",
                "recent",
                "statistics"
            ]
        }
