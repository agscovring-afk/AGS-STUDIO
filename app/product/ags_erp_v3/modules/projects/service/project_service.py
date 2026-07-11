class ProjectModule:

    name = "PROJECTS"

    def __init__(self):
        self.projects = []

    def add_project(self, project):
        self.projects.append(project)

    def list_projects(self):
        return self.projects
