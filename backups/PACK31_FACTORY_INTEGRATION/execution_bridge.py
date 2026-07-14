from app.ai.autonomous.agent_router import AgentRouter
from enterprise_builder.core.autonomous_executor_bridge import AutonomousEnterpriseExecutor


class ExecutionBridge:


    def __init__(self):

        self.router = AgentRouter()
        self.enterprise_executor = AutonomousEnterpriseExecutor()



    def execute_task(self, task):

        name = getattr(
            task,
            "name",
            str(task)
        )


        enterprise_tasks = {


            "design_enterprise_architecture":
                "design_enterprise_architecture",


            "design_facade_erp_architecture":
                "design_enterprise_architecture",


            "create_erp_modules":
                "create_erp_modules",


            "build_tenant_system":
                "build_tenant_system",


            "build_tender_management":
                "create_erp_modules",


            "generate_enterprise_release":
                "generate_enterprise_release",


            "validate_enterprise":
                "validate_enterprise",


            "validate_construction_platform":
                "validate_enterprise"

        }


        if name == "generate_construction_modules":

            return self.router.execute(
                task
            )



        if name in enterprise_tasks:


            class EnterpriseTask:


                def __init__(self,n):

                    self.name = n



            return self.enterprise_executor.run(
                EnterpriseTask(
                    enterprise_tasks[name]
                )
            )



        return self.router.execute(task)



execution_bridge = ExecutionBridge()
