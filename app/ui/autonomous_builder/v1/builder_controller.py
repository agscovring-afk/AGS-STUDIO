class BuilderController:

    def __init__(self):
        self.session = None

    def attach(self, session):
        self.session = session

    def build(self, request):
        if self.session:
            return self.session.run(request)

        return None
