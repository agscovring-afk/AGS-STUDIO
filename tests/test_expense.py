def test_expense_category_and_entry(tmp_path):
    from app.repositories.expense_repository import ExpenseRepository
    from app.controllers.expense_controller import ExpenseController

    db_file = tmp_path / "expenses.db"
    repo = ExpenseRepository(str(db_file))
    controller = ExpenseController(repo)
    controller.init_db()

    cat_id = controller.create_category(company_id=1, name="Travel", description="Travel expenses")
    eid = controller.create_expense(company_id=1, category_id=cat_id, amount=123.45, date="2026-07-01", project_id=1, supplier_id=None, payment_method="cash", notes="Taxi")
    assert eid == 1
    e = controller.get_expense(eid)
    assert e.amount == 123.45
