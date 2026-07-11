class UISelfBuildLoop:

    def __init__(self):
        self.history = []


    def create(self, specification):

        ui = {
            "specification": specification,
            "status": "created"
        }

        self.history.append(ui)

        return ui


    def modify(self, ui, changes):

        ui["changes"] = changes

        return ui


    def validate(self, ui):

        ui["validation"] = "passed"

        return ui
