from .base_worker import BaseWorker


class UIWorker(BaseWorker):

    name = "UI_WORKER"


    def execute(self, task):

        result = {
            "screens": [],
            "components": [],
            "navigation": []
        }

        return self.report(task, result)
