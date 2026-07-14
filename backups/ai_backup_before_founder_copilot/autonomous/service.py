"""
app/ai/autonomous/service.py
"""

from __future__ import annotations

from .controller import AutonomousController
from .active import AutonomousActive


class AutonomousService:

    def __init__(self, context):

        self.controller = AutonomousController(
            context
        )

        self.active = AutonomousActive(
            context
        )


    def run(self):

        self.active.analyze_project()

        return self.controller.start()


    def analyze(self):

        return self.active.analyze_project()


    def create_tasks(self, objective):

        return self.active.create_tasks(
            objective
        )


    def status(self):

        return {
            "running": True,
            "service": "AGS Autonomous AI",
            "mode": "active intelligence",
        }