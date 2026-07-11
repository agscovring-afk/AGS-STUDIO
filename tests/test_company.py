def test_company_repo_create_and_get(tmp_path):
    from app.repositories.company_repository import CompanyRepository
    from app.services.company_service import CompanyService
    from app.models.company import Company

    db_file = tmp_path / "test.db"
    repo = CompanyRepository(str(db_file))
    repo.create_tables()

    service = CompanyService(repo)
    company = Company(
        name="Legal Ltd",
        commercial_name="Legal",
        currency="DZD",
        language="fr"
    )
    company.set_code("COM-00001")

    cid = service.create_company(company)
    assert cid.lastrowid == 1

    retrieved = service.get_company(1)
    assert retrieved["name"] == "Legal Ltd"
    assert retrieved["code"] == "COM-00001"


def test_company_list_and_deactivate(tmp_path):
    from app.repositories.company_repository import CompanyRepository
    from app.services.company_service import CompanyService
    from app.models.company import Company

    db_file = tmp_path / "test2.db"
    repo = CompanyRepository(str(db_file))
    repo.create_tables()

    service = CompanyService(repo)

    c1 = Company(name="A")
    c1.set_code("COM-00001")
    c2 = Company(name="B")
    c2.set_code("COM-00002")

    service.create_company(c1)
    service.create_company(c2)

    all_comp = service.list_companies()
    assert len(all_comp) == 2

    service.deactivate_company(1)
    active = service.list_companies()
    assert len(active) == 1
