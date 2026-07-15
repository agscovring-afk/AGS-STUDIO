class EnterpriseAIRegistry:


    def __init__(self):

        self.actions={}



    def register(self,name,handler):

        self.actions[name]=handler



    def get(self,name):

        return self.actions.get(name)



    def list(self):

        return list(
            self.actions.keys()
        )