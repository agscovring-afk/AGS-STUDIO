class AIPanel:

    def __init__(self, title="AI"):

        self.title = title
        self.messages = []

    def append(self, message):

        self.messages.append(message)
