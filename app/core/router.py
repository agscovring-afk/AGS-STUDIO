"""
AGS ERP V2
UI Router
"""


class Router:

    def __init__(self):

        self.routes = {}


    def register(self, name, page):

        self.routes[name] = page


    def navigate(self, name):

        if name in self.routes:
            return self.routes[name]

        raise Exception(
            f"Route not found: {name}"
        )
