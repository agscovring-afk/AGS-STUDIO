from app.ai.self_developer.requirement import Requirement


class RequirementAnalyzer:

    def analyze(self,text):

        return Requirement(

            name=text.lower().replace(" ","_"),

            description=text

        )
