class RuntimeState:

    def __init__(self):

        self.status = "idle"
        self.history = []


    def update(self, status):

        self.status = status
        self.history.append(status)
