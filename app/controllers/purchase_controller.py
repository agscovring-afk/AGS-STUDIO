from app.repositories.purchase_repository import PurchaseRepository
from app.models.purchase import Purchase
from app.models.purchase_line import PurchaseLine


class PurchaseController:
    def __init__(self, repo: PurchaseRepository):
        self.repo = repo

    def init_db(self):
        self.repo.create_tables()

    def create_purchase(self, **fields) -> int:
        p = Purchase(**fields)
        return self.repo.add_purchase(p)

    def add_line(self, purchase_id: int, line_no: int, item_type: str, item_id: int = None, description: str = "", quantity: float = 0.0, unit_price: float = 0.0) -> int:
        total = quantity * unit_price
        pl = PurchaseLine(purchase_id=purchase_id, line_no=line_no, item_type=item_type, item_id=item_id, description=description, quantity=quantity, unit_price=unit_price, total=total)
        return self.repo.add_line(pl)

    def get_purchase(self, purchase_id: int):
        return self.repo.get_purchase(purchase_id)

    def list_by_supplier(self, supplier_id: int):
        return self.repo.list_purchases_by_supplier(supplier_id)
