"""
app/ai/autonomous/runner.py
"""

from __future__ import annotations

from .bootstrap import AutonomousBootstrap


class AutonomousRunner:

    def __init__(self, context):

        self.bootstrap = AutonomousBootstrap(
            context
        )


    def run(self):

        registry = self.bootstrap.load()

        api = registry.get(
            "api"
        )

        return api.execute()