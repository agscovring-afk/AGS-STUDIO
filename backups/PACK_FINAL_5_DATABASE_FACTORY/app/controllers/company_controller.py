"""
AGS ERP V2
Company Controller
"""

from app.core.base_controller import BaseController


class CompanyController(BaseController):

    def __init__(self, service):
        super().__init__(service)


    def create_company(self, company):

        return self.service.create_company(company)


    def get_company(self, company_id):

        return self.service.get_company(company_id)


    def get_companies(self):

        return self.service.list_companies()


    def update_company(self, company):

        return self.service.update_company(company)


    def deactivate_company(self, company_id):

        return self.service.deactivate_company(company_id)
