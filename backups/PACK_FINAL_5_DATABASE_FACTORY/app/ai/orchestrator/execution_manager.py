class ExecutionManager:


    def execute(self, task):

        return {
            "execution":
            "STARTED",
            "task":
            task
        }


manager = ExecutionManager()
