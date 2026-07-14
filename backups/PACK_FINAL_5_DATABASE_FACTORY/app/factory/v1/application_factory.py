class ApplicationFactory:

    def __init__(self):

        self.products = []


    def create(self, blueprint):

        app = {
            "name": blueprint,
            "status": "generated"
        }

        self.products.append(app)

        return app
