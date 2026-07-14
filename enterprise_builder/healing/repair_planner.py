
class RepairPlanner:

    def create_plan(self, errors):

        plan = []

        for error in errors:

            plan.append(
                {
                    "action": "repair",
                    "target": error
                }
            )

        return plan
