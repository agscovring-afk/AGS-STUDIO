"""
AGS ERP V2
Main Window
"""

import customtkinter as ctk

from app.core.router import Router
from app.ui.pages.clients_page import ClientsPage


class MainWindow(ctk.CTk):

    def __init__(self):

        super().__init__()


        self.title(
            "AGS ERP V2 Enterprise"
        )


        self.geometry(
            "1200x700"
        )


        self.router = Router()


        self.router.register(
            "clients",
            ClientsPage
        )


        self.container = ctk.CTkFrame(
            self
        )

        self.container.pack(
            fill="both",
            expand=True
        )


        self.show_page(
            "clients"
        )



    def show_page(
        self,
        name
    ):

        for widget in self.container.winfo_children():

            widget.destroy()


        page = self.router.navigate(
            name
        )


        frame = page(
            self.container
        )


        frame.pack(
            fill="both",
            expand=True
        )
