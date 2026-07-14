"""
app/ai/autonomous/api.py
"""

from __future__ import annotations

from .service import AutonomousService


class AutonomousAPI:

    def __init__(self, context):

        self.service = AutonomousService(
            context
        )


    def execute(self):

        return self.service.run()


    def analyze_project(self):

        return self.service.analyze()


    def create_tasks(self, objective):

        return self.service.create_tasks(
            objective
        )


    def health(self):

        return {
            "system": "AGS Autonomous",
            "status": "online",
        }