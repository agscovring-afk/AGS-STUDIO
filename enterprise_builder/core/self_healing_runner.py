
from enterprise_builder.healing.self_healing_engine import SelfHealingEngine


class SelfHealingRunner:

    def __init__(self):
        self.engine = SelfHealingEngine()


    def run(self, validation):

        return self.engine.heal(
            validation
        )
