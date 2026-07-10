"""
app/ai/autonomous/monitor.py
"""

from __future__ import annotations

from datetime import datetime

from .context import AutonomousContext


class AutonomousMonitor:

    def __init__(self, context: AutonomousContext):
        self.context = context

    def snapshot(self):

        state = self.context.snapshot

        return {
            "time": datetime.now().isoformat(),
            "tasks": len(state.tasks),
            "pending": len(state.pending_tasks),
            "failed": len(state.failed_tasks),
            "completed": len(state.completed_tasks),
            "statistics": state.statistics,
        }

    def health(self):

        state = self.context.snapshot

        if state.failed_tasks:
            return {
                "status": "warning",
                "message": "Failed tasks detected",
            }

        return {
            "status": "healthy",
            "message": "Autonomous system running normally",
        }