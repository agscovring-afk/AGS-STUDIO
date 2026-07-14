class BuilderSession:

    def __init__(self):

        self.history = []


    def run(self, request):

        self.history.append(request)

        return {
            "status": "completed",
            "request": request
        }
