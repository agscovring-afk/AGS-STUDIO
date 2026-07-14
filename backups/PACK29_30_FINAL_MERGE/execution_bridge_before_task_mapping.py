
from app.ai.autonomous.agent_router import AgentRouter
from enterprise_builder.core.autonomous_executor_bridge import AutonomousEnterpriseExecutor


class ExecutionBridge:


    def __init__(self):

        self.router = AgentRouter()
        self.enterprise_executor = AutonomousEnterpriseExecutor()



    def execute_task(self, task):

        name = getattr(task, "name", str(task))


        if name in [
            "design_enterprise_architecture",
            "create_erp_modules",
            "build_tenant_system",
            "generate_enterprise_release",
            "validate_enterprise"
        ]:

            return self.enterprise_executor.run(task)


        return self.router.execute(task)



execution_bridge = ExecutionBridge()
