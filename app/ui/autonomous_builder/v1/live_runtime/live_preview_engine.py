class LivePreviewEngine:

    def __init__(self):

        self.preview = None


    def render(self, application):

        self.preview = application

        return self.preview


    def refresh(self):

        return self.preview
