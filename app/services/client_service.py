"""
AGS ERP V2
Client Service
"""

from app.core.base_service import BaseService


class ClientService(BaseService):

    def __init__(
        self,
        repository
    ):

        super().__init__(
            repository
        )


    def create_client(
        self,
        client
    ):

        return self.repository.create(
            client
        )


    def list_clients(
        self
    ):

        return self.repository.list_all()


    def get_client(
        self,
        code
    ):

        return self.repository.get_by_code(
            code
        )


    def deactivate_client(
        self,
        client_id
    ):

        return self.repository.deactivate(
            client_id
        )
