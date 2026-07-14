class PlannerValidator:

    def validate(self, plan):

        if plan.total_phases() == 0:

            raise RuntimeError("Execution plan is empty.")

        for phase in plan.phases():

            if len(phase.tasks) == 0:

                raise RuntimeError(
                    f"Phase '{phase.name}' contains no tasks."
                )

        return True
