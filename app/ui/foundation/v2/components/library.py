class ComponentLibrary:

    def __init__(self):

        self.components = {}

    def add(self, name, component):

        self.components[name] = component

    def get(self, name):

        return self.components.get(name)
