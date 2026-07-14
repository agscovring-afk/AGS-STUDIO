from app.ai.improvement.performance_analyzer import analyzer
from app.ai.improvement.improvement_planner import planner
from app.ai.improvement.optimization_engine import engine


class SelfImprovement:

    def run(self, system):

        analysis = analyzer.analyze(system)
        plan = planner.plan(analysis)

        return engine.optimize(plan)


improvement = SelfImprovement()
