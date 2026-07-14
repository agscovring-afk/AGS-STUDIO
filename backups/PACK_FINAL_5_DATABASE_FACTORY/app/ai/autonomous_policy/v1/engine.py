class AutonomousPolicyEngine:
    def check(self,data):
        return {
            "engine":"AUTONOMOUS_POLICY_ENGINE_V1",
            "status":"checked",
            "policy":data
        }
