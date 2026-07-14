class BaseWorker:

    name = "BASE_WORKER"


    def execute(self, task):
        raise NotImplementedError(
            "Worker must implement execute()"
        )


    def report(self, task, result):

        return {
            "worker": self.name,
            "task": task,
            "status": "completed",
            "result": result
        }
