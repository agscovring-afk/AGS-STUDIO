class DecisionStrategy:


    def select(self, evaluation):

        mapping = {

            "ARCHITECTURE":
                "Architect Agent",

            "DATABASE":
                "Database Agent",

            "BACKEND":
                "Backend Agent",

            "UI":
                "UI Agent",

            "GENERAL":
                "Master Agent"
        }


        agent = mapping.get(
            evaluation["category"],
            "Master Agent"
        )


        return {
            "agent": agent,
            "strategy": evaluation["category"],
            "confidence": 95
        }


strategy = DecisionStrategy()