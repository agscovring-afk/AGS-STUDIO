from datetime import datetime


class OrchestratorRuntime:

    def __init__(self):

        self.status = "idle"
        self.started_at = None
        self.finished_at = None
        self.context = {}
        self.logs = []


    def start(self, context=None):

        self.status = "running"

        self.started_at = str(
            datetime.now()
        )

        self.context = context or {}

        self.log(
            "Runtime started"
        )


    def finish(self):

        self.status = "completed"

        self.finished_at = str(
            datetime.now()
        )

        self.log(
            "Runtime completed"
        )


    def fail(self, error):

        self.status = "failed"

        self.log(
            str(error)
        )


    def log(self, message):

        self.logs.append({

            "time": str(
                datetime.now()
            ),

            "message": message

        })


    def report(self):

        return {

            "status": self.status,

            "started_at": self.started_at,

            "finished_at": self.finished_at,

            "context": self.context,

            "logs": self.logs

        }