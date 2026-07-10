"""
app/ai/autonomous/controller.py
"""

from __future__ import annotations

from .loop import AutonomousLoop
from .monitor import AutonomousMonitor
from .reporter import AutonomousReporter


class AutonomousController:

    def __init__(self, context):

        self.context = context

        self.loop = AutonomousLoop(
            context
        )

        self.monitor = AutonomousMonitor(
            context
        )

        self.reporter = AutonomousReporter()


    def start(self, cycles=10):

        result = self.loop.run(
            max_cycles=cycles
        )

        report = {
            "result": result,
            "monitor": self.monitor.snapshot(),
            "health": self.monitor.health(),
        }

        self.reporter.generate(
            report
        )

        return report