from .workflow import Workflow
from .monitor import monitor


class WorkflowEngine:


    def create(self, name, steps):

        workflow = Workflow(name)

        for step in steps:

            workflow.add_step(step)


        monitor.record(
            f"Workflow created: {name}"
        )

        return workflow



    def run(self, workflow):

        workflow.start()

        monitor.record(
            f"Workflow started: {workflow.name}"
        )

        return workflow.data()



workflow_engine = WorkflowEngine()