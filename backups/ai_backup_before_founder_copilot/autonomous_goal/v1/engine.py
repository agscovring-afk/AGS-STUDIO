class AutonomousGoalEngine:
    def define(self,request):
        return {
            "engine":"AUTONOMOUS_GOAL_ENGINE_V1",
            "status":"defined",
            "goal":request
        }
