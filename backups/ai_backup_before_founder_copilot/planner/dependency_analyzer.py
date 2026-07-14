class DependencyAnalyzer:


    def analyze(self, tasks):

        dependencies = {}

        for task in tasks:

            dependencies[task] = []


        return {
            "dependencies": dependencies,
            "status": "ANALYZED"
        }


analyzer = DependencyAnalyzer()
