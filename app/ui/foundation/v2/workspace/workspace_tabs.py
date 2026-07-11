class WorkspaceTabs:

    def __init__(self):

        self.tabs = []
        self.active = None

    def open(self, name):

        self.tabs.append(name)
        self.active = name

    def close(self, name):

        if name in self.tabs:
            self.tabs.remove(name)
