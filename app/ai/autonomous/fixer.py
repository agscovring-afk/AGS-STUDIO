"""
app/ai/autonomous/fixer.py
"""

from __future__ import annotations

from .context import AutonomousContext
from .models import TaskStatus


class TaskFixer:

    def __init__(self, context: AutonomousContext):
        self.context = context

    def fix(self):

        fixed = 0

        for task in self.context.snapshot.failed_tasks:

            if task.retries >= task.max_retries:
                continue

            task.retries += 1
            task.status = TaskStatus.PENDING
            task.result = {}

            fixed += 1

        return {
            "fixed": fixed,
            "remaining_failed": len(self.context.snapshot.failed_tasks),
        }

    def reset_all(self):

        for task in self.context.snapshot.tasks:

            task.status = TaskStatus.PENDING
            task.retries = 0
            task.result = {}

        return len(self.context.snapshot.tasks)