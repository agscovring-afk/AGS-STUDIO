from datetime import datetime


class DecisionLog:


    def __init__(self):

        self.logs = []


    def add(self, decision):

        self.logs.append(
            {
                "decision": decision,
                "time": datetime.now().isoformat()
            }
        )


    def history(self):

        return self.logs


decision_log = DecisionLog()