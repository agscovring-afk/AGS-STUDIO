from .execution_plan import ExecutionPlan


class TaskScheduler:

    def __init__(self):

        self.plan = ExecutionPlan()

    def schedule(self, phase):

        self.plan.add_phase(phase)

    def build(self):

        return self.plan

    def clear(self):

        self.plan.clear()
