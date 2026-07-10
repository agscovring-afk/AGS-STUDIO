"""
app/ai/autonomous/task_generator.py
"""

from .models import Task


class TaskGenerator:
    """
    Converts user requests into autonomous tasks
    """

    def generate(self, request: str):

        tasks = []

        request_lower = request.lower()


        if "مناق" in request or "tender" in request_lower:

            tasks.extend([

                Task(
                    name="analyze_tender_workflow",
                    description="تحليل دورة تسيير المناقصات داخل الشركة",
                    priority=10
                ),

                Task(
                    name="design_tender_database",
                    description="تصميم قاعدة بيانات المناقصات والمشاريع",
                    priority=9
                ),

                Task(
                    name="create_tender_modules",
                    description="تحديد وحدات النظام المطلوبة",
                    priority=8
                ),

                Task(
                    name="generate_system_plan",
                    description="إنشاء خطة تنفيذ النظام",
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