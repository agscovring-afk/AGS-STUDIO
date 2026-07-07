from app.repositories.project_repository import ProjectRepository
from app.models.project import Project
from app.models.task import Task
from datetime import datetime


class ProjectController:
    def __init__(self, repo: ProjectRepository):
        self.repo = repo

    def init_db(self):
        self.repo.create_tables()

    def create_project(self, **fields) -> int:
        p = Project(**fields)
        return self.repo.add_project(p)

    def get_project(self, project_id: int):
        return self.repo.get_project(project_id)

    def create_task(self, project_id: int, title: str, **kwargs) -> int:
        t = Task(project_id=project_id, title=title, **kwargs)
        return self.repo.add_task(t)

    def list_tasks(self, project_id: int):
        return self.repo.list_tasks(project_id)
