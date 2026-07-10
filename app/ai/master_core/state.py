class MasterState:


    def __init__(self):

        self.status = "INITIALIZED"
        self.tasks = []


    def add_task(self,task):

        self.tasks.append(task)


state = MasterState()