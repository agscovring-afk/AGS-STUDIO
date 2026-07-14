from .task_graph import task_graph
from .dependency import dependency_manager


class AutonomousPlanner:


    def create_plan(self, request):

        tasks = []


        if "erp" in request.lower():

            tasks = [
                "Analyze ERP Requirements",
                "Design Database Architecture",
                "Create Backend Services",
                "Generate UI Modules",
                "Run System Validation",
                "Create Final Report"
            ]

        else:

            tasks = [
                "Analyze Request",
                "Create Solution",
                "Validate Result"
            ]


        for index, task in enumerate(tasks):

            task_graph.add_task(
                index + 1,
                task
            )


        dependency_manager.build(
            tasks
        )


        return {
            "request": request,
            "steps": tasks,
            "total_steps": len(tasks)
        }



planner = AutonomousPlanner()