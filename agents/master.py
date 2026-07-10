import os
import sys

# Add project root
PROJECT_ROOT = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


from app.ai.autonomous.engine import AutonomousEngine
from app.ai.autonomous.task_generator import TaskGenerator


class MasterAgent:
    """
    AGS Autonomous V2

    Flow:

    User Request
        |
        v
    Task Generator
        |
        v
    Autonomous Context
        |
        v
    Autonomous Brain
        |
        v
    Executor Loop
    """


    def __init__(self):

        self.name = "AGS MASTER AI"

        self.autonomous_engine = AutonomousEngine(
            "data/autonomous_state.json"
        )

        self.task_generator = TaskGenerator()



    def add_tasks(self, tasks):

        self.autonomous_engine.context.snapshot.tasks.extend(
            tasks
        )



    def process_request(self, user_request: str):

        print("\n================================")
        print(" MASTER AI PROCESSING REQUEST")
        print("================================")

        print(f"Request: {user_request}")


        # 1 - Generate Tasks

        tasks = self.task_generator.generate(
            user_request
        )


        print("\n[TASK GENERATOR]")

        for task in tasks:
            print(
                f"- {task.name} | priority={task.priority}"
            )


        # 2 - Inject Tasks into Autonomous Brain

        self.add_tasks(tasks)



        # 3 - Run Autonomous Cycle

        result = self.autonomous_engine.run()



        print("\n[AUTONOMOUS ENGINE STATUS]")

        print(result)



        return {

            "request": user_request,

            "tasks_created": len(tasks),

            "status": result

        }



    def status(self):

        return self.autonomous_engine.status()



if __name__ == "__main__":


    agent = MasterAgent()


    response = agent.process_request(
        "حلل نظام تسيير المناقصات لشركة مقاولات"
    )


    print("\n================================")
    print(" MASTER RESPONSE COMPLETE")
    print("================================")


    print(response)