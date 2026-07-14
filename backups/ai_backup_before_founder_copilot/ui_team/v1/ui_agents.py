class UIArchitectAgent:

    def design(self, request):

        return {
            "role": "architect",
            "request": request
        }


class UXAgent:

    def optimize(self, ui):

        return ui


class TestingAgent:

    def test(self, ui):

        return {
            "status": "tested",
            "ui": ui
        }
