"""
AGS Decision Intelligence Engine
"""

from datetime import datetime


class DecisionIntelligence:


    def __init__(self, knowledge):
        self.knowledge = knowledge



    def analyze(self, request):

        history = self.knowledge.search(
            request
        )


        return {

            "request":
            request,

            "previous_executions":
            len(history),

            "recommended_action":
            self.recommend(history),

            "timestamp":
            str(datetime.now())

        }



    def recommend(self, history):

        if not history:
            return "new_execution"


        return "reuse_previous_knowledge"



decision_intelligence = None
