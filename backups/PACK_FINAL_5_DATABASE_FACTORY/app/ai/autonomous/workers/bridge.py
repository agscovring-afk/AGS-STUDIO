from .registry import registry


class WorkerBridge:


    def dispatch(self, worker_name, task):

        worker = registry.get(worker_name)


        if not worker:

            return {
                "status": "error",
                "message": f"Worker {worker_name} not found"
            }


        return worker.execute(task)



bridge = WorkerBridge()
