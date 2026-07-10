def test_user_role_permission(tmp_path):
    from app.repositories.user_repository import UserRepository
    from app.controllers.user_controller import UserController

    db_file = tmp_path / "users.db"
    repo = UserRepository(str(db_file))
    controller = UserController(repo)
    controller.init_db()

    rid = controller.create_role("Admin", "Administrator")
    pid = controller.create_permission("companies.create", "Create companies")
    controller.assign_permission_to_role(rid, pid)

    uid = controller.create_user("alice", "alice@example.com", "Secret123!", company_id=1, role_id=rid)
    assert uid == 1
    assert controller.authenticate("alice", "Secret123!") is True
    assert controller.authenticate("alice", "wrong") is False
