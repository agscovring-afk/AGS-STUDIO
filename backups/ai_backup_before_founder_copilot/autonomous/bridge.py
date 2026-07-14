"""
app/ai/autonomous/bridge.py
"""

from __future__ import annotations


class AutonomousBridge:

    def __init__(self, context):

        self.context = context


    def send_task(self, task):

        self.context.snapshot.tasks.append(
            task
        )

        return {
            "status": "accepted",
            "task": task,
        }


    def get_state(self):

        snapshot = self.context.snapshot

        return {
            "tasks": len(snapshot.tasks),
            "pending": len(snapshot.pending_tasks),
            "failed": len(snapshot.failed_tasks),
            "completed": len(snapshot.completed_tasks),
        }