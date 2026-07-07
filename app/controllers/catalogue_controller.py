from app.repositories.catalogue_repository import CatalogueRepository
from app.models.category import Category
from app.models.unit import Unit
from app.models.product import Product
from app.models.service import Service


class CatalogueController:
    def __init__(self, repo: CatalogueRepository):
        self.repo = repo

    def init_db(self):
        self.repo.create_tables()

    # Categories
    def create_category(self, company_id: int, name: str, parent_id: int = None, description: str = "") -> int:
        cat = Category(company_id=company_id, name=name, parent_id=parent_id, description=description)
        return self.repo.add_category(cat)

    def list_categories(self):
        return self.repo.list_categories()

    # Units
    def create_unit(self, name: str, symbol: str, conversion_factor: float = 1.0) -> int:
        u = Unit(name=name, symbol=symbol, conversion_factor=conversion_factor)
        return self.repo.add_unit(u)

    def list_units(self):
        return self.repo.list_units()

    # Products
    def create_product(self, company_id: int, code: str, name: str, category_id: int = None, unit_id: int = None, cost_price: float = 0.0, sale_price: float = 0.0, tax_rate: float = 0.0, stock_tracked: bool = False) -> int:
        p = Product(company_id=company_id, code=code, name=name, category_id=category_id, unit_id=unit_id, cost_price=cost_price, sale_price=sale_price, tax_rate=tax_rate, stock_tracked=stock_tracked)
        return self.repo.add_product(p)

    def get_product(self, product_id: int):
        return self.repo.get_product(product_id)

    def search_products(self, term: str):
        return self.repo.search_products(term)

    # Services
    def create_service(self, company_id: int, code: str, name: str, category_id: int = None, unit_id: int = None, default_price: float = 0.0, tax_rate: float = 0.0) -> int:
        s = Service(company_id=company_id, code=code, name=name, category_id=category_id, unit_id=unit_id, default_price=default_price, tax_rate=tax_rate)
        return self.repo.add_service(s)

    def get_service(self, service_id: int):
        return self.repo.get_service(service_id)

    def search_services(self, term: str):
        return self.repo.search_services(term)
