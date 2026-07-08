"""
AGS ERP V2
Client Page
"""

import customtkinter as ctk

from app.ui.components.app_table import AppTable


class ClientsPage(ctk.CTkFrame):

    def __init__(
        self,
        parent,
        controller=None
    ):

        super().__init__(
            parent
        )

        self.controller = controller


        title = ctk.CTkLabel(
            self,
            text="Clients",
            font=("Arial",24)
        )

        title.pack(
            pady=20
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


    def refresh(self):

        if self.controller:

            data = self.controller.get_clients()

            self.table.load_data(
                data
            )
