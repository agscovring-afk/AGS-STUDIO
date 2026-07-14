
class CloudDeploymentV2:

    def execute(self,request):

        return {
            "engine":"AGS CLOUD DEPLOYMENT FACTORY V2",
            "docker":"READY",
            "server":"READY",
            "cloud":"READY",
            "release":"READY",
            "status":"COMPLETED"
        }


bridge=CloudDeploymentV2()
