class ComponentMarketplace:

    def __init__(self):

        self.components = {}


    def publish(self,name,component):

        self.components[name]=component


    def search(self,name):

        return self.components.get(name)
