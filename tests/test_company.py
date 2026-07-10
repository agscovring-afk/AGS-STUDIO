def test_company_repo_create_and_get(tmp_path):
    from app.repositories.company_repository import CompanyRepository
    from app.controllers.company_controller import CompanyController

    db_file = tmp_path / "test.db"
    repo = CompanyRepository(str(db_file))
    controller = CompanyController(repo)
    controller.init_db()
    cid = controller.create_company("Legal Ltd", "Legal", "COM-00001", "DZD", "fr")
    assert cid == 1
    company = controller.get_company(1)
    assert company.legal_name == "Legal Ltd"
    assert company.code == "COM-00001"


def test_company_list_and_deactivate(tmp_path):
    from app.repositories.company_repository import CompanyRepository
    from app.controllers.company_controller import CompanyController

    db_file = tmp_path / "test2.db"
    repo = CompanyRepository(str(db_file))
    controller = CompanyController(repo)
    controller.init_db()
    controller.create_company("A", "A", "COM-00001", "DZD", "fr")
    controller.create_company("B", "B", "COM-00002", "DZD", "fr")
    all_comp = controller.list_companies()
    assert len(all_comp) == 2
    controller.deactivate_company(1)
    active = controller.list_companies()
    assert len(active) == 1
    inactive_all = controller.list_companies(include_inactive=True)
    assert len(inactive_all) == 2
