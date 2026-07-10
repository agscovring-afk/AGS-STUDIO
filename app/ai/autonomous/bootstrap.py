"""
app/ai/autonomous/bootstrap.py
"""

from __future__ import annotations

from .registry import AutonomousRegistry
from .api import AutonomousAPI
from .bridge import AutonomousBridge


class AutonomousBootstrap:

    def __init__(self, context):

        self.context = context

        self.registry = AutonomousRegistry()


    def load(self):

        api = AutonomousAPI(
            self.context
        )

        bridge = AutonomousBridge(
            self.context
        )

        self.registry.register(
            "api",
            api
        )

        self.registry.register(
            "bridge",
            bridge
        )

        return self.registry


    def status(self):

        return {
            "system": "AGS Autonomous V2",
            "loaded": True,
        }