"""
app/ai/autonomous/active.py
"""

from __future__ import annotations

from .scanner import ProjectScanner
from .task_generator import TaskGenerator


class AutonomousActive:

    def __init__(self, context):

        self.context = context

        self.scanner = ProjectScanner(
            context
        )

        self.generator = TaskGenerator(
            context
        )


    def analyze_project(self):

        return self.scanner.scan()


    def create_tasks(self, objective):

        return self.generator.generate(
            objective
        )