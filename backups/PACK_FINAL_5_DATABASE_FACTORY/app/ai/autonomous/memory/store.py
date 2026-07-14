class MemoryStore:


    def __init__(self):

        self.storage = {}


    def save(self, key, data):

        self.storage[key] = data


    def load(self, key):

        return self.storage.get(key)


    def all(self):

        return self.storage



store = MemoryStore()