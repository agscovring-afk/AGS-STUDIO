"""
app/ai/autonomous/brain.py
"""

from __future__ import annotations

from typing import Optional

from .context import AutonomousContext
from .models import Task, TaskStatus


class AutonomousBrain:


    def __init__(self, context: AutonomousContext):

        self.context = context



    def next_task(self) -> Optional[Task]:

        tasks = [

            t for t in self.context.snapshot.tasks

            if t.status == TaskStatus.PENDING

        ]


        if not tasks:

            return None


        tasks.sort(
            key=lambda t: int(t.priority),
            reverse=True
        )

        return tasks[0]



    def mark_running(self, task: Task):

        task.status = TaskStatus.RUNNING



    def mark_success(self, task: Task):

        task.status = TaskStatus.COMPLETED



    def mark_failed(self, task: Task):

        task.status = TaskStatus.FAILED



    def has_pending_tasks(self):

        return any(

            t.status == TaskStatus.PENDING

            for t in self.context.snapshot.tasks

        )



    def summary(self):

        return {

            "pending": len(
                [
                    t for t in self.context.snapshot.tasks
                    if t.status == TaskStatus.PENDING
                ]
            ),

            "running": len(
                [
                    t for t in self.context.snapshot.tasks
                    if t.status == TaskStatus.RUNNING
                ]
            ),

            "completed": len(
                [
                    t for t in self.context.snapshot.tasks
                    if t.status == TaskStatus.COMPLETED
                ]
            ),

            "failed": len(
                [
                    t for t in self.context.snapshot.tasks
                    if t.status == TaskStatus.FAILED
                ]
            ),
        }