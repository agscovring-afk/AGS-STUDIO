"""
app/ai/autonomous/decision.py
"""

from __future__ import annotations


class AutonomousDecision:

    def __init__(self, context):
        self.context = context

    def evaluate(self, task):

        if task.priority >= 8:

            return {
                "action": "execute",
                "reason": "high priority task",
            }

        if task.retries > 0:

            return {
                "action": "retry",
                "reason": "failed task recovery",
            }

        return {
            "action": "execute",
            "reason": "normal execution",
        }