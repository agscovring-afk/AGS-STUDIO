
import subprocess

from enterprise_builder.healing.repair_history import RepairHistory
from enterprise_builder.core.release_report import ReleaseReport


class AutonomousRepairLoop:


    def __init__(
        self,
        validator,
        healing_engine,
        repair_planner,
        fixer_engine,
        max_cycles=5
    ):

        self.validator = validator
        self.healing_engine = healing_engine
        self.repair_planner = repair_planner
        self.fixer_engine = fixer_engine

        self.max_cycles = max_cycles

        self.history = RepairHistory()
        self.report = ReleaseReport()


    def run(self, target_path="."):

        result = {
            "status": "started",
            "cycles": 0,
            "fixed": []
        }


        for cycle in range(self.max_cycles):

            result["cycles"] = cycle + 1

            validation = self.validator.validate(
                target_path
            )


            if validation.get("success", False):

                result["status"] = "released"

                self.report.create(
                    result
                )

                return result


            errors = validation.get(
                "errors",
                []
            )


            analysis = self.healing_engine.analyze(
                errors
            )


            plan = self.repair_planner.create_plan(
                analysis
            )


            repaired = self.fixer_engine.apply(
                plan
            )


            result["fixed"].extend(
                repaired
            )


            self.history.save(
                {
                    "cycle": cycle + 1,
                    "errors": errors,
                    "fixed": repaired
                }
            )


            subprocess.run(
                [
                    "python",
                    "-m",
                    "compileall",
                    target_path
                ],
                capture_output=True,
                text=True
            )


        result["status"] = "failed"

        self.report.create(
            result
        )

        return result
