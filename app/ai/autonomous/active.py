"""
AGS Autonomous V2
Active Intelligence Layer
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

        tasks = self.generator.generate(
            objective
        )

        self.context.snapshot.tasks.extend(
            tasks
        )

        self.context.save()

        return tasks
