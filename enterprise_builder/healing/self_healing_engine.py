
from .error_detector import ErrorDetector
from .repair_planner import RepairPlanner
from .fixer_engine import FixerEngine


class SelfHealingEngine:


    def __init__(self):

        self.detector = ErrorDetector()
        self.planner = RepairPlanner()
        self.fixer = FixerEngine()



    def heal(self, validation_result):

        errors = self.detector.detect(
            validation_result
        )

        if not errors:

            return {
                "status": "healthy",
                "repairs": []
            }


        plan = self.planner.create_plan(
            errors
        )


        fixes = self.fixer.fix(
            plan
        )


        return {
            "status": "healed",
            "repairs": fixes
        }
