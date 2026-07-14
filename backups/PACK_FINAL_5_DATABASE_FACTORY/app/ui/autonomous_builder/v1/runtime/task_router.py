class TaskRouter:

    def __init__(self):

        self.routes = {}


    def register(self, name, handler):

        self.routes[name] = handler


    def route(self, name, payload=None):

        handler = self.routes.get(name)

        if handler:

            return handler(payload)


        return None
