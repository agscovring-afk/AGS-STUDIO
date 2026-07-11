class UIMemoryEngine:

    def __init__(self):

        self.memory = []


    def store(self, design):

        self.memory.append(design)


    def recall(self):

        return self.memory
