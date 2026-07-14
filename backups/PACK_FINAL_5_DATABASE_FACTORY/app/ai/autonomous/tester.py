"""
app/ai/autonomous/tester.py
"""

from __future__ import annotations


class AutonomousTester:

    def __init__(self, context):

        self.context = context


    def run(self):

        tests = {
            "context": self.test_context(),
            "tasks": self.test_tasks(),
        }

        return tests


    def test_context(self):

        return self.context is not None


    def test_tasks(self):

        return hasattr(
            self.context.snapshot,
            "tasks"
        )