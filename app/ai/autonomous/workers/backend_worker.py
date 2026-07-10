from .base_worker import BaseWorker


class BackendWorker(BaseWorker):

    name = "BACKEND_WORKER"


    def execute(self, task):

        result = {
            "api": "planned",
            "services": [],
            "controllers": []
        }

        return self.report(task, result)
