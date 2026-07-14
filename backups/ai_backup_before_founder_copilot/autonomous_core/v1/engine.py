from .planner import AutonomousTaskPlanner
from .executor import AutonomousExecutionEngine
from .validator import AutonomousValidator
from .fixer import AutonomousFixer
from .memory import AutonomousMemory
from .reporter import AutonomousReporter


class AutonomousCoreEngine:

    def __init__(self):
        self.planner = AutonomousTaskPlanner()
        self.executor = AutonomousExecutionEngine()
        self.validator = AutonomousValidator()
        self.fixer = AutonomousFixer()
        self.memory = AutonomousMemory()
        self.reporter = AutonomousReporter()

    def run(self, request):

        plan = self.planner.plan(request)
        execution = self.executor.execute(plan)
        validation = self.validator.validate(execution)

        self.memory.save(validation)

        return self.reporter.report(validation)
