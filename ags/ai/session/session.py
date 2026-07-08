from datetime import datetime


class AISession:


    def __init__(self, module):

        self.module = module
        self.started = str(datetime.now())
        self.context = {}
        self.responses = {}


    def add_response(self, agent, response):

        self.responses[agent] = response


    def to_dict(self):

        return {

            "module": self.module,
            "started": self.started,
            "context": self.context,
            "responses": self.responses

        }
