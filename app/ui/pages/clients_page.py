"""
AGS ERP V2
Client Page
"""

import customtkinter as ctk

from app.ui.components.app_table import AppTable
from app.ui.dialogs.client_dialog import ClientDialog
from app.models.client import Client
from app.repositories.client_repository import ClientRepository
from app.services.client_service import ClientService
from app.controllers.client_controller import ClientController


class ClientsPage(ctk.CTkFrame):

    def __init__(
        self,
        parent
    ):

        super().__init__(
            parent
        )


        repository = ClientRepository()

        service = ClientService(
            repository
        )

        self.controller = ClientController(
            service
        )


        title = ctk.CTkLabel(
            self,
            text="Clients",
            font=("Arial",24)
        )

        title.pack(
            pady=15
        )


        add_button = ctk.CTkButton(
            self,
            text="Add Client",
            command=self.open_dialog
        )

        add_button.pack(
            pady=10
        )


        self.table = AppTable(
            self,
            [
                "Code",
                "Name",
                "Phone",
                "City"
            ]
        )

        self.table.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )


        self.refresh()



    def refresh(self):

        clients = self.controller.get_clients()

        self.table.load_data(
            clients
        )



    def open_dialog(self):

        ClientDialog(
            self,
            self.save_client
        )



    def save_client(
        self,
        data
    ):

        client = Client(
            name=data["name"],
            phone=data["phone"]
        )


        self.controller.create_client(
            client
        )


        self.refresh()
