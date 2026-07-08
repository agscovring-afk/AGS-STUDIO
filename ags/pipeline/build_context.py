from datetime import datetime


class BuildContext:


    def __init__(self, module):

        self.module = module
        self.started = str(datetime.now())
        self.results = {}
        self.logs = []
        self.errors = []
        self.metadata = {}


    def add_result(self, name, result):

        self.results[name] = result
        self.logs.append(
            f"{name} completed"
        )


    def add_error(self, error):

        self.errors.append(
            error
        )


    def to_dict(self):

        return {

            "module": self.module,
            "started": self.started,
            "results": self.results,
            "logs": self.logs,
            "errors": self.errors,
            "metadata": self.metadata

        }
