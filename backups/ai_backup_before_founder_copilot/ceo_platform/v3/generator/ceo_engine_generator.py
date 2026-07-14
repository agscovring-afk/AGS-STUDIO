from app.ai.generator.ags_module_generator import ModuleGenerator


class CEOEngineGenerator:

    def __init__(self):
        self.generator = ModuleGenerator()


    def build_phase(self, name):

        module = f"ceo_{name}"

        return self.generator.create(module)


generator = CEOEngineGenerator()