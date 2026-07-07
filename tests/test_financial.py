def test_numbering_and_documents(tmp_path):
    from app.repositories.financial_repository import FinancialRepository
    from app.controllers.financial_controller import FinancialController

    db_file = tmp_path / "fin.db"
    repo = FinancialRepository(str(db_file))
    controller = FinancialController(repo)
    controller.init_db()

    qid = controller.create_quotation(company_id=1, client_id=1, lines=[{"item_type":"product","quantity":2,"unit_price":100}])
    assert qid == 1
    iid = controller.create_invoice(company_id=1, client_id=1, lines=[{"item_type":"product","quantity":3,"unit_price":200}])
    assert iid == 1
    pay_id = controller.record_payment(invoice_id=iid, amount=100.0)
    assert pay_id == 1
