class DependencyManager:


    def __init__(self):

        self.dependencies = []


    def build(self, tasks):

        self.dependencies = []

        for i in range(len(tasks)-1):

            self.dependencies.append(
                {
                    "before": tasks[i],
                    "after": tasks[i+1]
                }
            )


        return self.dependencies


    def get(self):

        return self.dependencies



dependency_manager = DependencyManager()