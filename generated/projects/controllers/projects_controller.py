from ..services.projects_service import ProjectsService


class ProjectsController:


    def __init__(self):
        self.service = ProjectsService()
