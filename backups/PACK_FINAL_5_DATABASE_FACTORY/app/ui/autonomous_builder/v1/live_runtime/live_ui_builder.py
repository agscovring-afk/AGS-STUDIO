class LiveUIBuilder:

    def __init__(self, designer=None):

        self.designer = designer
        self.current_ui = None


    def connect_designer(self, designer):

        self.designer = designer


    def build(self, specification):

        self.current_ui = {
            "specification": specification,
            "status": "built"
        }

        return self.current_ui


    def update(self, change):

        if self.current_ui:

            self.current_ui["update"] = change

        return self.current_ui
