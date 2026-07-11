class AGSGlobalApplicationFactory:


    def __init__(self):

        self.apps=[]


    def generate(self,specification):

        app={
            "specification": specification,
            "status":"global_factory_generated"
        }

        self.apps.append(app)

        return app
