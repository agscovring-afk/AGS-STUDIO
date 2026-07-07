"""
AGS ERP V2
Company Service
"""

from app.core.base_service import BaseService


class CompanyService(BaseService):

    def __init__(self, repository, numbering_service=None):
        super().__init__(repository)
        self.numbering_service = numbering_service

    def create_company(self, company):

        if self.numbering_service:
            code = self.numbering_service.generate(
                "company",
                "COM"
            )
            company.set_code(code)

        return self.repository.create(company)

    def get_company(self, company_id):
        return self.repository.get(company_id)

    def list_companies(self):
        return self.repository.list_all()

    def deactivate_company(self, company_id):
        return self.repository.delete(company_id)
