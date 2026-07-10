class KnowledgeStore:


    def __init__(self):

        self.knowledge=[]


    def store(self, item):

        self.knowledge.append(item)


    def search(self):

        return self.knowledge


store = KnowledgeStore()
