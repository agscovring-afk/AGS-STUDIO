from .evaluator import evaluator
from .strategy import strategy
from .decision_log import decision_log


class DecisionEngine:

    def decide(self, task):

        evaluation = evaluator.evaluate(task)

        selected = strategy.select(
            evaluation
        )

        result = {
            "task": task,
            "evaluation": evaluation,
            "selected_agent": selected["agent"],
            "strategy": selected["strategy"],
            "confidence": selected["confidence"],
            "action": "DELEGATE"
        }

        decision_log.add(result)

        return result


decision_engine = DecisionEngine()