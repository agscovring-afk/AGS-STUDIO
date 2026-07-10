"""
AGS Autonomous V2
Real Execution Engine V2
"""

from __future__ import annotations

from .context import AutonomousContext
from .brain import AutonomousBrain
from .executor import TaskExecutor
from .models import TaskStatus



class AutonomousEngine:


    def __init__(self, project_root="."):

        self.context = AutonomousContext(project_root)

        self.brain = AutonomousBrain(
            self.context
        )

        self.executor = TaskExecutor(
            self.context
        )



    def initialize(self):

        self.context.update_statistics()

        self.context.save()

        return True



    def run(self):

        self.initialize()


        while self.brain.has_pending_tasks():

            task = self.brain.next_task()


            if task is None:

                break



            self.brain.mark_running(task)


            try:

                result = self.executor.execute(task)


                print(
                    "TASK RESULT:",
                    task.name,
                    result
                )



                if task.status == TaskStatus.COMPLETED:

                    self.brain.mark_success(task)


                else:

                    self.brain.mark_failed(task)



            except Exception as e:


                print(
                    "EXECUTION ERROR:",
                    task.name,
                    e
                )


                task.result = {
                    "error": str(e)
                }


                self.brain.mark_failed(task)



            self.context.update_statistics()

            self.context.save()



        return self.context.statistics()



    def status(self):

        return self.brain.summary()
