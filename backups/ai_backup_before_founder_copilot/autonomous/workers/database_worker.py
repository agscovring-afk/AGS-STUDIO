from .base_worker import BaseWorker


class DatabaseWorker(BaseWorker):

    name = "DATABASE_WORKER"


    def execute(self, task):

        result = {
            "database": "SQLite",
            "schema": "generated",
            "tables": []
        }

        return self.report(task, result)
