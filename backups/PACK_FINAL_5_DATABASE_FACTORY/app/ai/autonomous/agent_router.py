from app.ai.autonomous.agent_registry import registry


class AgentRouter:


    def __init__(self):

        self.registry = registry



    def resolve_agent(self, task):

        name = getattr(
            task,
            "name",
            ""
        ).lower()



        routes = {


            # Tender / ERP analysis

            "analyze_tender_workflow":
                "ARCHITECT_AGENT",

            "analyze_construction_domain":
                "ARCHITECT_AGENT",



            # Architecture

            "design_tender_database":
                "DATABASE_AGENT",

            "design_facade_erp_architecture":
                "ARCHITECT_AGENT",



            # Module generation

            "create_tender_modules":
                "MODULE_BUILDER_AGENT",

            "generate_construction_modules":
                "MODULE_BUILDER_AGENT",



            # Planning

            "generate_system_plan":
                "ARCHITECT_AGENT",



            # Validation

            "validate_construction_platform":
                "TESTING_AGENT",



            # Default

            "build_tender_management":
                "MODULE_BUILDER_AGENT"

        }



        return routes.get(
            name,
            "MODULE_BUILDER_AGENT"
        )




    def execute(self, task):

        agent_name = self.resolve_agent(
            task
        )


        agent = self.registry.get(
            agent_name
        )


        if not agent:

            return {
                "status":"no_agent",
                "agent":agent_name,
                "task":getattr(task,"name",task)
            }



        if hasattr(agent,"execute"):

            return agent.execute(task)



        if hasattr(agent,"analyze"):

            return agent.analyze(task)



        return {
            "status":"unknown_agent_interface",
            "agent":agent_name
        }



router = AgentRouter()
