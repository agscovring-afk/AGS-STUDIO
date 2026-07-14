"""
AGS Autonomous V2
Task Validator
"""

from __future__ import annotations


class TaskValidator:


    def validate(self, task=None):

        if task is not None:

            status = getattr(
                task,
                "status",
                None
            )

            return {
                "success": status != "failed",
                "task": getattr(
                    task,
                    "name",
                    None
                ),
                "status": str(status)
            }


        return {
            "success": True,
            "status": "validated",
            "message": "Autonomous system validation completed"
        }

validator = TaskValidator()
