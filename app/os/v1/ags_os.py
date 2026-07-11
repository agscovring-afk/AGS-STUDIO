class AGSOperatingSystem:


    def __init__(self):

        self.modules={}


    def load(self,name,module):

        self.modules[name]=module


    def run(self):

        return "AGS OS RUNNING"
