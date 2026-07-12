
class Router:

    def __init__(self, workspace):
        self.workspace = workspace
        self.routes = {}

    def register(self, name, page):
        self.routes[name] = page

    def navigate(self, name):
        if name in self.routes:
            page = self.routes[name]()
            self.workspace.show(page)
            return True

        return False
