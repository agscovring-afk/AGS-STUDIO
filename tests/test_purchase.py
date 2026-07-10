def test_purchase_and_lines(tmp_path):
    from app.repositories.purchase_repository import PurchaseRepository
    from app.controllers.purchase_controller import PurchaseController

    db_file = tmp_path / "purchases.db"
    repo = PurchaseRepository(str(db_file))
    controller = PurchaseController(repo)
    controller.init_db()

    pid = controller.create_purchase(company_id=1, code="PUR-0001", supplier_id=1, date="2026-07-07", status="ordered", total=0.0)
    assert pid == 1
    l1 = controller.add_line(purchase_id=pid, line_no=1, item_type="product", item_id=1, description="Sheets", quantity=50, unit_price=20)
    l2 = controller.add_line(purchase_id=pid, line_no=2, item_type="product", item_id=2, description="Screws", quantity=200, unit_price=0.1)
    p = controller.get_purchase(pid)
    assert p.code == "PUR-0001"
