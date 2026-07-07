"""Controller for company operations."""
from app.repositories.company_repository import CompanyRepository
from app.models.company import Company
from datetime import datetime


class CompanyController:
    def __init__(self, repo: CompanyRepository):
        self.repo = repo

    def init_db(self):
        self.repo.create_table()

    def create_company(self, legal_name: str, commercial_name: str, code: str, currency: str, language: str) -> int:
        company = Company(
            id=0,
            legal_name=legal_name,
            commercial_name=commercial_name,
            code=code,
            currency=currency,
            language=language,
            is_active=True,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        return self.repo.add(company)

    def get_company(self, company_id: int):
        return self.repo.get(company_id)

    def list_companies(self, include_inactive: bool = False):
        return self.repo.list_all(include_inactive=include_inactive)

    def update_company(self, company_id: int, **fields):
        comp = self.repo.get(company_id)
        if not comp:
            raise ValueError("Company not found")
        for k, v in fields.items():
            if hasattr(comp, k):
                setattr(comp, k, v)
        comp.updated_at = datetime.utcnow()
        self.repo.update(comp)

    def deactivate_company(self, company_id: int):
        self.repo.deactivate(company_id)
