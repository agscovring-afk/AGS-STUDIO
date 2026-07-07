from app.models.company import Company
from app.repositories.company_repository import CompanyRepository
from app.services.company_service import CompanyService
from app.services.numbering_service import NumberingService


repo = CompanyRepository()

numbering = NumberingService()

service = CompanyService(
    repo,
    numbering
)


company = Company(
    name="AGS COVERING",
    commercial_name="AGS"
)

service.create_company(company)

print("Company created:", company.code)

companies = service.list_companies()

for c in companies:
    print(dict(c))
