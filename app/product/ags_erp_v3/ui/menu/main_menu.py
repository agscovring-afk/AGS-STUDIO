class MainMenu:

    def __init__(self):
        self.items = []

    def add(self, name):
        self.items.append(name)

    def list(self):
        return self.items
