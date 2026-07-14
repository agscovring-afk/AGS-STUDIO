
class TaskGenerationIntelligence:


    def generate(self, request):

        print("\n[TASK GENERATION INTELLIGENCE]")


        tasks = []


        text = request.lower()


        if "erp" in text:

            tasks = [

                {
                    "name": "analyze_erp_requirements",
                    "description": "Analyze ERP business requirements",
                    "agent": "ARCHITECT_AGENT"
                },

                {
                    "name": "design_database_architecture",
                    "description": "Design ERP database architecture",
                    "agent": "DATABASE_AGENT"
                },

                {
                    "name": "create_backend_modules",
                    "description": "Create backend ERP modules",
                    "agent": "BACKEND_AGENT"
                },

                {
                    "name": "generate_ui_modules",
                    "description": "Generate ERP user interface modules",
                    "agent": "UI_AGENT"
                },

                {
                    "name": "validate_system",
                    "description": "Run system validation",
                    "agent": "TESTING_AGENT"
                }

            ]


        elif "construction" in text:

            tasks = [

                {
                    "name": "analyze_construction_workflow",
                    "description": "Analyze construction workflow",
                    "agent": "ARCHITECT_AGENT"
                },

                {
                    "name": "create_project_management_module",
                    "description": "Create project management module",
                    "agent": "BACKEND_AGENT"
                }

            ]


        else:

            tasks = [

                {
                    "name": "analyze_request",
                    "description": request,
                    "agent": "ARCHITECT_AGENT"
                }

            ]


        print(
            f"[TASKS GENERATED] {len(tasks)}"
        )


        return tasks



task_generator_intelligence = TaskGenerationIntelligence()
