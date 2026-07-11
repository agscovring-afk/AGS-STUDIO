class AGSMarketplace:


    def __init__(self):

        self.items={}


    def publish(self,name,item):

        self.items[name]=item


    def get(self,name):

        return self.items.get(name)
