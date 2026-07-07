"""Controller for client operations."""
from app.repositories.client_repository import ClientRepository
from app.models.client import Client
from datetime import datetime


class ClientController:
    def __init__(self, repo: ClientRepository):
        self.repo = repo

    def init_db(self):
        self.repo.create_table()

    def create_client(self, legal_name: str, commercial_name: str, code: str, currency: str, language: str) -> int:
        client = Client(
            id=0,
            legal_name=legal_name,
            commercial_name=commercial_name,
            code=code,
            currency=currency,
            language=language,
            is_active=True,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        return self.repo.add(client)

    def get_client(self, client_id: int):
        return self.repo.get(client_id)

    def list_companies(self, include_inactive: bool = False):
        return self.repo.list_all(include_inactive=include_inactive)

    def update_client(self, client_id: int, **fields):
        comp = self.repo.get(client_id)
        if not comp:
            raise ValueError("Client not found")
        for k, v in fields.items():
            if hasattr(comp, k):
                setattr(comp, k, v)
        comp.updated_at = datetime.utcnow()
        self.repo.update(comp)

    def deactivate_client(self, client_id: int):
        self.repo.deactivate(client_id)






