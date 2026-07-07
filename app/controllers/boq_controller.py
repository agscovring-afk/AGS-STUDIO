from app.repositories.boq_repository import BOQRepository
from app.models.boq import BOQ
from app.models.boq_line import BOQLine
from datetime import datetime


class BOQController:
    def __init__(self, repo: BOQRepository):
        self.repo = repo

    def init_db(self):
        self.repo.create_tables()

    def create_boq(self, project_id: int, code: str, title: str, description: str = "") -> int:
        b = BOQ(project_id=project_id, code=code, title=title, description=description)
        return self.repo.add_boq(b)

    def add_line(self, boq_id: int, line_no: int, item_type: str, item_id: int = None, description: str = "", quantity: float = 0.0, unit_id: int = None, unit_price: float = 0.0) -> int:
        total = quantity * unit_price
        line = BOQLine(boq_id=boq_id, line_no=line_no, item_type=item_type, item_id=item_id, description=description, quantity=quantity, unit_id=unit_id, unit_price=unit_price, total=total)
        return self.repo.add_line(line)

    def list_boqs(self, project_id: int):
        return self.repo.list_boqs_for_project(project_id)

    def get_lines(self, boq_id: int):
        return self.repo.get_lines(boq_id)
