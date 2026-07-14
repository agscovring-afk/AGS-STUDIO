
from enterprise_builder.healing.self_healing_engine import SelfHealingEngine


class SelfHealingPlugin:

    def __init__(self):
        self.engine = SelfHealingEngine()


    def heal(self, validation_result):

        return self.engine.heal(
            validation_result
        )
