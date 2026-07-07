"""
AGS ERP V2
Company CRUD Test
"""

from app.models.company import Company
from app.repositories.company_repository import CompanyRepository
from app.services.company_service import CompanyService
from app.services.numbering_service import NumberingService


repository = CompanyRepository()

numbering = NumberingService()

service = CompanyService(
    repository,
    numbering
)


print("=== CREATE ===")

company = Company(
    name="TEST COMPANY",
    commercial_name="TEST"
)

service.create_company(company)

print("Created:", company.code)


print("\n=== LIST ===")

companies = service.list_companies()

for item in companies:
    print(dict(item))


print("\n=== UPDATE ===")

company.id = 1
company.phone = "0550000000"
company.email = "test@ags.com"

service.update_company(company)

updated = service.get_company(1)

print(dict(updated))


print("\n=== DEACTIVATE ===")

service.deactivate_company(1)

companies = service.list_companies()

for item in companies:
    print(dict(item))


print("\nDONE")
