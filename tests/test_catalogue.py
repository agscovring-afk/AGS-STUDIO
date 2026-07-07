def test_catalogue_create_and_search(tmp_path):
    from app.repositories.catalogue_repository import CatalogueRepository
    from app.controllers.catalogue_controller import CatalogueController

    db_file = tmp_path / "catalogue.db"
    repo = CatalogueRepository(str(db_file))
    controller = CatalogueController(repo)
    controller.init_db()

    cid = controller.create_category(company_id=1, name="Materials")
    uid = controller.create_unit(name="Meter", symbol="m", conversion_factor=1.0)
    pid = controller.create_product(company_id=1, code="PRD-0001", name="Aluminium Profile", category_id=cid, unit_id=uid, cost_price=100.0, sale_price=150.0, tax_rate=19.0, stock_tracked=True)
    sid = controller.create_service(company_id=1, code="SRV-0001", name="Installation", default_price=50.0, tax_rate=19.0)

    p = controller.get_product(pid)
    assert p.name == "Aluminium Profile"
    s = controller.get_service(sid)
    assert s.name == "Installation"

    prods = controller.search_products("Aluminium")
    assert len(prods) == 1
    servs = controller.search_services("Install")
    assert len(servs) == 1
