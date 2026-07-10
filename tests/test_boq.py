def test_boq_and_lines(tmp_path):
    from app.repositories.boq_repository import BOQRepository
    from app.controllers.boq_controller import BOQController

    db_file = tmp_path / "boq.db"
    repo = BOQRepository(str(db_file))
    controller = BOQController(repo)
    controller.init_db()

    bid = controller.create_boq(project_id=1, code="BOQ-0001", title="BOQ Phase 1")
    assert bid == 1
    l1 = controller.add_line(boq_id=bid, line_no=1, item_type="product", item_id=1, description="Profile", quantity=10, unit_id=1, unit_price=100)
    l2 = controller.add_line(boq_id=bid, line_no=2, item_type="service", item_id=1, description="Install", quantity=5, unit_id=None, unit_price=50)
    lines = controller.get_lines(bid)
    assert len(lines) == 2
    assert lines[0].total == 1000
