class MemoryIndex:


    def __init__(self):

        self.index = {}


    def add(self, category, key):

        if category not in self.index:
            self.index[category] = []

        self.index[category].append(key)


    def search(self, category):

        return self.index.get(
            category,
            []
        )



memory_index = MemoryIndex()