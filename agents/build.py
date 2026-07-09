from agents.base_agent import AIEnabledAgent

from app.ai.orchestrator.core.workflow import Workflow
from app.ai.orchestrator.core.step import WorkflowStep
from app.ai.orchestrator.queue.task_queue import TaskQueue
from app.ai.orchestrator.runtime.runtime import OrchestratorRuntime
from app.ai.orchestrator.executor.executor import WorkflowExecutor


class BuildAgent(AIEnabledAgent):

    def __init__(self):

        super().__init__("build")

        self.runtime = OrchestratorRuntime()

        self.queue = TaskQueue()

        self.executor = WorkflowExecutor()


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

        workflow = self.create_workflow(module)

        result = self.executor.execute(
            workflow,
            module
        )


        try:

            result["ai"] = self.ask_ai(
                f"Create implementation plan for ERP module '{module}'",
                session
            )

        except Exception as e:

            result["ai_error"] = str(e)


        return {

            "module": module,

            "status": "build_completed",

            "execution": result

        }
