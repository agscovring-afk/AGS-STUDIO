"""
app/ai/autonomous/doctor.py
"""

from __future__ import annotations

from .diagnostics import AutonomousDiagnostics
from .tester import AutonomousTester
from .health import AutonomousHealth


class AutonomousDoctor:

    def __init__(self, context):

        self.context = context

        self.diagnostics = AutonomousDiagnostics(
            context
        )

        self.tester = AutonomousTester(
            context
        )

        self.health = AutonomousHealth(
            context
        )


    def run(self):

        return {
            "diagnostics": self.diagnostics.summary(),
            "tests": self.tester.run(),
            "health": self.health.check(),
        }