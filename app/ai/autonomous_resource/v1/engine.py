class AutonomousResourceEngine:
    def manage(self,data):
        return {
            "engine":"AUTONOMOUS_RESOURCE_ENGINE_V1",
            "status":"managed",
            "resources":data
        }
