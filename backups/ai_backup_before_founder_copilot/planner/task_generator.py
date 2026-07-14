class TaskGenerator:


    def generate(self, request):

        tasks = [
            "SYSTEM_ARCHITECTURE",
            "DATABASE_DESIGN",
            "BACKEND_DEVELOPMENT",
            "UI_DEVELOPMENT",
            "SYSTEM_TESTING"
        ]

        return {
            "request": request,
            "tasks": tasks,
            "count": len(tasks)
        }


generator = TaskGenerator()
