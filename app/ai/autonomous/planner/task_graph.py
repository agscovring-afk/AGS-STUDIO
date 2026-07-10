class TaskGraph:


    def __init__(self):

        self.tasks = []


    def add_task(self, id, name):

        self.tasks.append(
            {
                "id": id,
                "name": name,
                "status": "PENDING"
            }
        )


    def complete(self, id):

        for task in self.tasks:

            if task["id"] == id:
                task["status"] = "COMPLETED"


    def all(self):

        return self.tasks



task_graph = TaskGraph()