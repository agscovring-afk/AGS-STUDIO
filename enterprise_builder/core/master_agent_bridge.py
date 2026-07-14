from enterprise_builder.core.autonomous_loop import EnterpriseAutonomousLoop


class MasterAgentEnterpriseBridge:


    def __init__(self):

        self.loop = EnterpriseAutonomousLoop()



    def process(self, request):

        keywords=[
            "erp",
            "enterprise",
            "business",
            "platform",
            "system",
            "company",
            "construction",
            "contractor",
            "tender",
            "project",
            "projects",
            "inventory",
            "stock",
            "supplier",
            "suppliers",
            "facade",
            "aluminium",
            "glass",
            "\u0645\u0642\u0627\u0648\u0644\u0627\u062a",
            "\u0645\u0646\u0627\u0642\u0635\u0629",
            "\u0645\u0646\u0627\u0642\u0635\u0627\u062a",
            "\u0645\u0634\u0627\u0631\u064a\u0639",
            "\u0645\u062e\u0632\u0648\u0646",
            "\u0645\u0648\u0631\u062f\u064a\u0646"
        ]


        if any(
            k in request.lower()
            for k in keywords
        ):

            return self.loop.run(
                request
            )


        return {
            "status":"NO_ENTERPRISE_ACTION",
            "request":request
        }