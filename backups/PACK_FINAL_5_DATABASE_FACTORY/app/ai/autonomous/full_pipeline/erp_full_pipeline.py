from app.ai.autonomous.orchestrator.orchestrator import orchestrator
from app.ai.autonomous.erp_executor.erp_auto_executor import executor


class ERPFullBuildPipeline:


    def execute(self, request):


        intelligence = orchestrator.execute(
            request
        )


        modules = [

            "companies",
            "clients",
            "projects",
            "tenders",
            "boq",
            "quotations",
            "invoices",
            "payments",
            "purchases",
            "warehouse",
            "reports",
            "users",
            "permissions"

        ]


        build = executor.execute(
            modules
        )


        return {

            "pipeline":
            "AUTONOMOUS ERP FULL BUILD PIPELINE V1",

            "request":
            request,

            "engines":
            intelligence["count"],

            "modules":
            build["modules"],

            "status":
            "completed"

        }



pipeline = ERPFullBuildPipeline()
