"""
AGS ERP V2
Client Controller
"""

from app.core.base_controller import BaseController


class ClientController(BaseController):


    def create_client(
        self,
        client
    ):

        return self.service.create_client(
            client
        )


    def get_clients(
        self
    ):

        return self.service.list_clients()


    def deactivate(
        self,
        client_id
    ):

        return self.service.deactivate_client(
            client_id
        )
