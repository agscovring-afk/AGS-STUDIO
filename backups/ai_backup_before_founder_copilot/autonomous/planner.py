"""
app/ai/autonomous/planner.py
"""

from __future__ import annotations


class AutonomousPlanner:

    def __init__(self, context):

        self.context = context


    def create_plan(self, objective):

        tasks = []

        for step in objective:

            tasks.append(
                {
                    "name": step,
                    "status": "pending",
                }
            )

        return tasks


    def add_task(self, task):

        self.context.snapshot.tasks.append(
            task
        )

        return task
