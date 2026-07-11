class ProjectContext:

    def __init__(self, project=None):
        self.project = project
        self.modules = []
        self.dependencies = []
        self.metadata = {}
        self.runtime = {}

    def add_module(self, module):
        self.modules.append(module)

    def add_dependency(self, dependency):
        self.dependencies.append(dependency)

    def set_metadata(self, key, value):
        self.metadata[key] = value

    def set_runtime(self, key, value):
        self.runtime[key] = value

    def export(self):
        return {
            "project": self.project,
            "modules": self.modules,
            "dependencies": self.dependencies,
            "metadata": self.metadata,
            "runtime": self.runtime
        }
