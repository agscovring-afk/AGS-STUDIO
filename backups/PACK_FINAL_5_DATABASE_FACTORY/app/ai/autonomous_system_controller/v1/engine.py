class AutonomousSystemController:
    def control(self,data):
        return {"engine":"AUTONOMOUS_SYSTEM_CONTROLLER_V1","status":"controlled","system":data}
