class DecisionEngine:


    def decide(self, request):

        if "ERP" in request.upper():

            return {
                "decision":
                    "BUILD_ENTERPRISE_SYSTEM",
                "priority":
                    "HIGH"
            }


        return {
            "decision":
                "GENERAL_AUTONOMOUS_TASK",
            "priority":
                "NORMAL"
        }


decision = DecisionEngine()
