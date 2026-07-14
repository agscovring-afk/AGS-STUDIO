from enterprise_builder.core.autonomous_bridge import EnterpriseAutonomousBridge
from enterprise_builder.core.autonomous_executor_bridge import AutonomousEnterpriseExecutor


class EnterpriseAutonomousLoop:


    def __init__(self):

        self.bridge = EnterpriseAutonomousBridge()
        self.executor = AutonomousEnterpriseExecutor()


    def run(self, request):

        result = self.bridge.execute_task(request)


        return {

            "status": "COMPLETED",

            "request": request,

            "result": result

        }
