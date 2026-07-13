"""
app/ai/autonomous/task_generator.py
"""

from .models import Task


class TaskGenerator:
    """
    Converts user requests into autonomous tasks
    """

    def __init__(self, context=None):
        self.context = context

    def _exists(self, name, description):

        if not self.context:
            return False

        return any(
            t.name == name
            for t in self.context.snapshot.tasks
        )

    def generate(self, request: str):

        tasks = []

        request_lower = request.lower()

        def add_task(name, description, priority):

            if not self._exists(name, description):

                tasks.append(
                    Task(
                        name=name,
                        description=description,
                        priority=priority
                    )
                )

        if "tender" in request_lower or "????" in request:

            add_task("analyze_tender_workflow", "Analyze tender workflow", 10)
            add_task("design_tender_database", "Design tender database", 9)
            add_task("create_tender_modules", "Create tender modules", 8)
            add_task("generate_system_plan", "Generate system_plan", 7)

        else:

            add_task(
                "general_analysis",
                request,
                5
            )

        return tasks
