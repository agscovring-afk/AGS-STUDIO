from app.ai.self_developer.engine import SelfDeveloper
from app.generators.module_generator import ModuleGenerator


class DevelopmentPipeline:

    def __init__(self):

        self.ai = SelfDeveloper()

        self.generator = ModuleGenerator()


    def create(self, requirement):

        analysis = self.ai.analyze(requirement)

        module = analysis["requirement"]["name"]

        generated = self.generator.create(module)

        return {

            "analysis": analysis,

            "generated": generated

        }
