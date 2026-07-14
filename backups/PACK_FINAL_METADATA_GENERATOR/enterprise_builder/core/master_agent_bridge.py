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
            "system"
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