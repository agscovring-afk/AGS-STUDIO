class AGSCloudPlatform:


    def __init__(self):

        self.services = {}


    def register(self,name,service):

        self.services[name]=service


    def deploy(self,name):

        return self.services.get(name)
