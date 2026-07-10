from app.repositories.employee_repository import EmployeeRepository


class EmployeeController:

    def __init__(self, repo:EmployeeRepository):
        self.repo = repo
