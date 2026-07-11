PHASE_201 = [
    "AGS_PRODUCTION_REALITY_ENGINE"
]


class AGSPhase201ProductionEngine:

    def __init__(self):
        self.phase = PHASE_201
        self.status = "INITIALIZED"

    def start(self):
        self.status = "PRODUCTION_BUILD_READY"

        return {
            "phase": self.phase,
            "status": self.status
        }
