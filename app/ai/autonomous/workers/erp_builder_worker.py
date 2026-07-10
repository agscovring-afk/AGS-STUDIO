from .base_worker import BaseWorker


class ERPBuilderWorker(BaseWorker):

    name = "ERP_BUILDER_WORKER"


    def execute(self, task):

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


        return self.report(
            task,
            {
                "erp":
                "Construction ERP",

                "modules":
                modules,

                "count":
                len(modules)
            }
        )
