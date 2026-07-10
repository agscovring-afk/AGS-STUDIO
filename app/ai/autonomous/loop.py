"""
AGS Autonomous V2
Autonomous Execution Loop V2
"""

from __future__ import annotations

import time

from .context import AutonomousContext
from .brain import AutonomousBrain
from .executor import TaskExecutor
from .fixer import TaskFixer
from .validator import TaskValidator



class AutonomousLoop:


    def __init__(self, context: AutonomousContext):

        self.context = context

        self.brain = AutonomousBrain(context)

        self.executor = TaskExecutor(context)

        self.validator = TaskValidator()

        self.fixer = TaskFixer(context)



    def run(self, max_cycles: int = 10):

        cycle = 0


        while cycle < max_cycles:

            cycle += 1


            #
            # EXECUTION CYCLE
            #

            while self.brain.has_pending_tasks():


                task = self.brain.next_task()


                if task is None:
                    break


                result = self.executor.execute(task)



                #
                # stop on failed task
                #

                if task.status.name == "FAILED":

                    break



            #
            # GLOBAL VALIDATION
            #

            report = self.validator.validate()



            if report.get("success"):

                self.context.update_statistics()

                self.context.save()

                return report



            #
            # RECOVERY
            #

            fix_report = self.fixer.fix()


            self.context.update_statistics()

            self.context.save()



            if fix_report["fixed"] == 0:

                return report



            time.sleep(0.2)



        return self.validator.validate()