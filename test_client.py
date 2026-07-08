"""
AGS ERP V2
Client CRUD Test
"""

from app.models.client import Client
from app.repositories.client_repository import ClientRepository
from app.services.client_service import ClientService


repository = ClientRepository()

service = ClientService(
    repository
)


client = Client(
    name="TEST CLIENT",
    contact="Ahmed",
    function="Manager",
    phone="0555000000",
    email="client@test.com",
    city="Alger",
    wilaya="Alger",
    country="Algeria",
    rc="RC123456",
    nif="NIF123456",
    nis="NIS123456",
    ai="AI123456",
    bank="BNA",
    rib="000111222"
)





print("=== CREATE ===")


service.create_client(
    client
)


print("Client created")


print()
print("=== LIST ===")


clients = service.list_clients()


for c in clients:

    print(dict(c))
