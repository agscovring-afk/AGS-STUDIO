from .engine import UIAutonomousBuilderEngine
from .generator import UIGenerator
from .writer import UIWriter


class UIBuilderBridge:

    def __init__(self):
        self.engine = UIAutonomousBuilderEngine()
        self.generator = UIGenerator()
        self.writer = UIWriter()

    def execute(self, metadata):

        plan = self.engine.build(metadata)
        generated = self.generator.generate(plan)
        result = self.writer.write(generated)

        return {
            "system": "AGS UI AUTONOMOUS BUILDER V1",
            "plan": plan,
            "generation": generated,
            "writer": result,
            "status": "COMPLETED"
        }

    def status(self):
        return self.engine.status()


ui_builder = UIBuilderBridge()
