from app.repositories.expense_repository import ExpenseRepository
from app.models.expense import Expense
from app.models.expense_category import ExpenseCategory


class ExpenseController:
    def __init__(self, repo: ExpenseRepository):
        self.repo = repo

    def init_db(self):
        self.repo.create_tables()

    def create_category(self, company_id: int, name: str, description: str = "") -> int:
        cat = ExpenseCategory(company_id=company_id, name=name, description=description)
        return self.repo.add_category(cat)

    def create_expense(self, **fields) -> int:
        e = Expense(**fields)
        return self.repo.add_expense(e)

    def get_expense(self, expense_id: int):
        return self.repo.get_expense(expense_id)

    def list_by_project(self, project_id: int):
        return self.repo.list_expenses_by_project(project_id)
