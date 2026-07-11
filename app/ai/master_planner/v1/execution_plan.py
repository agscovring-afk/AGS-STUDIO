from .models import BuildPhase


class ExecutionPlan:

    def __init__(self):

        self._phases = []

    def add_phase(self, phase: BuildPhase):

        self._phases.append(phase)

    def phases(self):

        return self._phases

    def clear(self):

        self._phases.clear()

    def total_phases(self):

        return len(self._phases)

    def total_tasks(self):

        total = 0

        for phase in self._phases:

            total += len(phase.tasks)

        return total
