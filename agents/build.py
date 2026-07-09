from agents.base_agent import AIEnabledAgent

from app.ai.orchestrator.core.workflow import Workflow
from app.ai.orchestrator.core.step import WorkflowStep
from app.ai.orchestrator.queue.task_queue import TaskQueue
from app.ai.orchestrator.runtime.runtime import OrchestratorRuntime


class BuildAgent(AIEnabledAgent):

    def __init__(self):

        super().__init__("build")

        self.runtime = OrchestratorRuntime()

        self.queue = TaskQueue()


    def create_workflow(self, module):

        workflow = Workflow(
            name=f"{module}_build",
            description=f"Build ERP module {module}"
        )


        tasks = [

            ("architecture", "architect", "analyze"),

            ("database", "database", "create_schema"),

            ("backend", "backend", "generate_api"),

            ("ui", "ui", "generate_interface"),

            ("validation", "testing", "validate")

        ]


        for name, agent, action in tasks:

            step = WorkflowStep(

                name=name,

                agent=agent,

                action=action

            )

            workflow.add_step(step)

            self.queue.push(step)


        return workflow



    def analyze(self, module, session=None):

        self.runtime.start({

            "module": module

        })


        workflow = self.create_workflow(
            module
        )


        plan = {

            "module": module,

            "status": "build_started",

            "workflow": workflow.to_dict()

        }


        try:

            ai_result = self.ask_ai(

                f"Create a complete implementation plan for ERP module '{module}'",

                session

            )

            plan["ai"] = ai_result


            self.runtime.finish()


        except Exception as e:

            self.runtime.fail(e)

            plan["ai_error"] = str(e)


        plan["runtime"] = self.runtime.report()


        return plan