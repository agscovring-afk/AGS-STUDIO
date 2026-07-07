def test_client_crud_and_search(tmp_path):
    from app.repositories.client_repository import ClientRepository
    from app.controllers.client_controller import ClientController

    db_file = tmp_path / "clients.db"
    repo = ClientRepository(str(db_file))
    controller = ClientController(repo)
    controller.init_db()

    cid1 = controller.create_client(code="CLI-00001", name="Client A", company_id=1)
    cid2 = controller.create_client(code="CLI-00002", name="B Client", company_id=1)
    assert cid1 == 1
    c1 = controller.get_client(cid1)
    assert c1.name == "Client A"

    res = controller.search_clients("Client")
    assert len(res) == 2
