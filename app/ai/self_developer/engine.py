from app.ai.self_developer.analyzers.requirement_analyzer import RequirementAnalyzer
from app.ai.self_developer.builders.prompt_builder import PromptBuilder


class SelfDeveloper:

    def __init__(self):

        self.analyzer=RequirementAnalyzer()

        self.builder=PromptBuilder()

    def analyze(self,text):

        req=self.analyzer.analyze(text)

        return {

            "requirement":req.to_dict(),

            "prompt":self.builder.build(req)

        }
