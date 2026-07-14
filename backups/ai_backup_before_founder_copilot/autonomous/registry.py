"""
app/ai/autonomous/registry.py
"""

from __future__ import annotations


class AutonomousRegistry:

    def __init__(self):

        self.components = {}


    def register(self, name, component):

        self.components[name] = component

        return True


    def get(self, name):

        return self.components.get(
            name
        )


    def list(self):

        return list(
            self.components.keys()
        )