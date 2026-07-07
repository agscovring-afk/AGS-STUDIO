"""
AGS ERP V2
Main Window
"""

import customtkinter as ctk

from app.core.router import Router


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


        self.container = ctk.CTkFrame(
            self
        )

        self.container.pack(
            fill="both",
            expand=True
        )


    def show_page(self, page):

        for widget in self.container.winfo_children():
            widget.destroy()


        frame = page(
            self.container
        )

        frame.pack(
            fill="both",
            expand=True
        )
