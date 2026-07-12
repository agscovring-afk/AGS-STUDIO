
class Workspace:

    def __init__(self):
        self.current = None

    def show(self, page):
        self.current = page
        print("[WORKSPACE]", page)
