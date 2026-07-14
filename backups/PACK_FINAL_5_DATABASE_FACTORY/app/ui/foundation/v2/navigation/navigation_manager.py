class NavigationManager:

    def __init__(self):

        self.routes = {}

    def register(self, route, page):

        self.routes[route] = page

    def resolve(self, route):

        return self.routes.get(route)
