class DecisionMemory:


    def __init__(self):

        self.decisions=[]


    def add(self, decision):

        self.decisions.append(decision)


    def get(self):

        return self.decisions


memory = DecisionMemory()
