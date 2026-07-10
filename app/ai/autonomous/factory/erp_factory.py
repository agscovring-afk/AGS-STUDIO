class ERPFactory:


    def build(self, modules):

        plan = []


        for module in modules:

            plan.append(

                {
                    "module":
                    module
                }

            )


        return plan



factory = ERPFactory()
