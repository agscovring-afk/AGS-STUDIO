class AGSMasterController:
    def control(self,data):
        return {
            "engine":"AGS_MASTER_CONTROLLER_V1",
            "status":"running",
            "system":data
        }
