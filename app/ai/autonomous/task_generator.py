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



    def generate(self, request: str):

        tasks = []

        request_lower = request.lower()


        if "tender" in request_lower or "مناق" in request:


            tasks.extend([

                Task(
                    name="analyze_tender_workflow",
                    description="Analyze tender workflow",
                    priority=10
                ),

                Task(
                    name="design_tender_database",
                    description="Design tender database",
                    priority=9
                ),

                Task(
                    name="create_tender_modules",
                    description="Create tender modules",
                    priority=8
                ),

                Task(
                    name="generate_system_plan",
                    description="Generate system plan",
                    priority=7
                )

            ])


        else:

            tasks.append(

                Task(
                    name="general_analysis",
                    description=request,
                    priority=5
                )

            )


        return tasks
