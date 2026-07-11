def test_client_crud_and_search(tmp_path):
    from app.repositories.client_repository import ClientRepository
    from app.services.client_service import ClientService
    from app.models.client import Client

    db_file = tmp_path / "clients.db"
    repo = ClientRepository(str(db_file))
    repo.create_tables()

    service = ClientService(repo)

    c1 = Client(name="Client A")
    c1.company_id = 1
    c1.code = "CLI-00001"
    c2 = Client(name="B Client")
    c2.company_id = 1
    c2.code = "CLI-00002"

    cid1 = service.create_client(c1)
    cid2 = service.create_client(c2)

    assert cid1.lastrowid == 1

    retrieved = service.get_client("CLI-00001")
    assert retrieved["name"] == "Client A"

    clients = service.list_clients()
    assert len(clients) == 2
