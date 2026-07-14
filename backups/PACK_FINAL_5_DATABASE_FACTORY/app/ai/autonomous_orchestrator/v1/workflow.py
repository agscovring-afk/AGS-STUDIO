class Workflow:

    def __init__(self, request):
        self.request = request
        self.state = "CREATED"
        self.trace = []

    def update(self, state, data=None):
        self.state = state
        self.trace.append({
            "state": state,
            "data": data
        })
