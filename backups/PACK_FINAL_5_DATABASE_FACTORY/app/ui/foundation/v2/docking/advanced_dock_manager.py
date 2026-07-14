class AdvancedDockManager:

    def __init__(self):

        self.docks = {}

    def dock(self, name, position):

        self.docks[name] = position

    def layout(self):

        return self.docks
