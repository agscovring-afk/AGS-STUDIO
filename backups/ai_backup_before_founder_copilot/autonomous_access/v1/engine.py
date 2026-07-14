class AutonomousAccessEngine:
    def authorize(self,data):
        return {
            "engine":"AUTONOMOUS_ACCESS_ENGINE_V1",
            "status":"authorized",
            "access":data
        }
