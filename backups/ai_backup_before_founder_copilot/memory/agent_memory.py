class AgentMemory:


    def __init__(self):

        self.history={}


    def remember(self, agent, result):

        self.history[agent]=result


    def recall(self, agent):

        return self.history.get(agent)


memory = AgentMemory()
