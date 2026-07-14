from .models import BuildPhase, BuildTask


class PhaseRegistry:

    def __init__(self):

        self._phases = {}

    def register(self, phase: BuildPhase):

        self._phases[phase.name] = phase

    def get(self, name):

        return self._phases.get(name)

    def all(self):

        return list(self._phases.values())

    def exists(self, name):

        return name in self._phases

    def clear(self):

        self._phases.clear()
